"""
Auto-fixer para atomizacao de queries no rag_coverage_topics.json.

Uso:
  python -m scripts.fix_queries --dry-run
  python -m scripts.fix_queries --apply
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    backend_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Auto-fix de queries condensadas")
    parser.add_argument(
        "--topics-file",
        type=Path,
        default=backend_root / "scripts" / "rag_coverage_topics.json",
        help="Arquivo JSON de topicos (default: scripts/rag_coverage_topics.json)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Aplica alteracoes no arquivo; sem flag faz dry-run",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Executa sem gravar arquivo (default implicito).",
    )
    parser.add_argument(
        "--keep-umbrella",
        dest="keep_umbrella",
        action="store_true",
        default=True,
        help="Preserva query guarda-chuva de topico (default: true)",
    )
    parser.add_argument(
        "--no-keep-umbrella",
        dest="keep_umbrella",
        action="store_false",
        help="Nao adiciona query guarda-chuva de topico",
    )
    parser.add_argument(
        "--redundancy-distance-threshold",
        type=float,
        default=0.3,
        help="Threshold da distancia de Jaccard para dedupe (default: 0.3)",
    )
    parser.add_argument(
        "--only-groups",
        nargs="*",
        default=None,
        help="Lista opcional de group ids para aplicar (default: todos)",
    )
    return parser.parse_args()


def load_topics(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Arquivo de topicos nao encontrado: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("groups"), list):
        raise ValueError("Formato invalido: esperado objeto com lista em 'groups'.")
    return data


def normalize_text(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value)
    without_accents = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    lowered = without_accents.lower()
    cleaned = re.sub(r"[^a-z0-9+\s]", " ", lowered)
    return re.sub(r"\s+", " ", cleaned).strip()


def tokenize(value: str) -> set[str]:
    norm = normalize_text(value)
    if not norm:
        return set()
    return set(norm.split(" "))


def jaccard_distance(query_a: str, query_b: str) -> float:
    set_a = tokenize(query_a)
    set_b = tokenize(query_b)
    if not set_a and not set_b:
        return 0.0
    union = set_a | set_b
    if not union:
        return 0.0
    similarity = len(set_a & set_b) / len(union)
    return 1.0 - similarity


def concept_aliases(concept: str) -> list[str]:
    aliases = [concept]
    if ":" in concept:
        aliases.append(concept.split(":", 1)[0].strip())
    concept_norm = normalize_text(concept)
    parts = concept_norm.split(" ")
    if parts and re.fullmatch(r"d\d+", parts[0]):
        aliases.append(parts[0].upper())
    if ":" not in concept and len(parts) >= 2 and len(parts[-1]) >= 5:
        aliases.append(parts[-1])
    return [a for a in aliases if a]


def detect_concepts(query: str, concepts: list[str]) -> list[str]:
    norm_query = normalize_text(query)
    detected: list[str] = []
    for concept in concepts:
        matched = False
        for alias in concept_aliases(concept):
            alias_norm = normalize_text(alias)
            if alias_norm and f" {alias_norm} " in f" {norm_query} ":
                matched = True
                break
        if matched:
            detected.append(concept)
    return detected


def strip_detected_concepts(query: str, detected_concepts: list[str]) -> str:
    root = query
    for concept in detected_concepts:
        for alias in concept_aliases(concept):
            root = re.sub(re.escape(alias), " ", root, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", root).strip()


def clean_group_title(title: str) -> str:
    title = re.sub(r"^\d+\s+", "", title.strip())
    return title.lower()


def unique_stable(items: list[str]) -> list[str]:
    dedup: list[str] = []
    seen: set[str] = set()
    for item in items:
        norm = normalize_text(item)
        if not norm or norm in seen:
            continue
        seen.add(norm)
        dedup.append(item.strip())
    return dedup


def split_condensed_query(query: str, group_title: str, detected_concepts: list[str], keep_umbrella: bool) -> list[str]:
    if len(detected_concepts) < 2:
        return [query]

    root = strip_detected_concepts(query, detected_concepts)
    if not root:
        root = clean_group_title(group_title)

    generated: list[str] = []
    if keep_umbrella and root:
        generated.append(root)
    for concept in detected_concepts:
        generated.append(f"{root} {concept}".strip() if root else concept)
    return unique_stable(generated)


def classify_query(query: str, group_title: str, concepts: list[str]) -> tuple[str, list[str]]:
    detected = detect_concepts(query, concepts)
    if normalize_text(query) == normalize_text(clean_group_title(group_title)):
        return ("umbrella", detected)
    if len(tokenize(query)) <= 7:
        return ("topic_or_concept", detected)
    return ("action", detected)


def sort_queries(queries: list[str], group_title: str, concepts: list[str]) -> list[str]:
    buckets: dict[str, list[str]] = {"umbrella": [], "topic_or_concept": [], "action": []}
    for q in queries:
        category, _ = classify_query(q, group_title, concepts)
        buckets[category].append(q)
    return (
        sorted(unique_stable(buckets["umbrella"]), key=normalize_text)
        + sorted(unique_stable(buckets["topic_or_concept"]), key=normalize_text)
        + sorted(unique_stable(buckets["action"]), key=normalize_text)
    )


def dedupe_by_distance(queries: list[str], distance_threshold: float) -> list[str]:
    result: list[str] = []
    for query in queries:
        keep = True
        query_tokens = tokenize(query)
        for existing in result:
            existing_tokens = tokenize(existing)
            same_size = len(query_tokens) == len(existing_tokens)
            if same_size and jaccard_distance(query, existing) < distance_threshold:
                keep = False
                break
        if keep:
            result.append(query)
    return result


def transform_group(
    group: dict[str, Any],
    keep_umbrella: bool,
    redundancy_distance_threshold: float,
) -> tuple[list[str], list[str]]:
    group_title = str(group.get("title", ""))
    concepts = [str(c) for c in (group.get("concepts") or [])]
    original_queries = [str(q) for q in (group.get("queries") or [])]

    transformed: list[str] = []
    for query in original_queries:
        detected = detect_concepts(query, concepts)
        transformed.extend(split_condensed_query(query, group_title, detected, keep_umbrella))

    transformed = unique_stable(transformed)
    transformed = dedupe_by_distance(transformed, redundancy_distance_threshold)
    transformed = sort_queries(transformed, group_title, concepts)
    return original_queries, transformed


def build_diff(original: list[str], updated: list[str]) -> list[str]:
    lines: list[str] = []
    removed = [q for q in original if normalize_text(q) not in {normalize_text(u) for u in updated}]
    added = [q for q in updated if normalize_text(q) not in {normalize_text(o) for o in original}]
    for q in removed:
        lines.append(f"- {q}")
    for q in added:
        lines.append(f"+ {q}")
    return lines


def main() -> int:
    args = parse_args()
    data = load_topics(args.topics_file)
    groups = data["groups"]
    only_groups = set(args.only_groups or [])

    changed_groups = 0
    total_added = 0
    total_removed = 0

    for group in groups:
        group_id = str(group.get("id", "unknown"))
        if only_groups and group_id not in only_groups:
            continue

        original, updated = transform_group(
            group=group,
            keep_umbrella=args.keep_umbrella,
            redundancy_distance_threshold=args.redundancy_distance_threshold,
        )
        diff_lines = build_diff(original, updated)
        if not diff_lines:
            continue

        changed_groups += 1
        print(f"\n[{group_id}]")
        for line in diff_lines:
            print(line)

        total_added += sum(1 for line in diff_lines if line.startswith("+ "))
        total_removed += sum(1 for line in diff_lines if line.startswith("- "))
        group["queries"] = updated

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"\nModo: {mode}")
    print(f"Grupos alterados: {changed_groups}")
    print(f"Queries adicionadas: {total_added}")
    print(f"Queries removidas: {total_removed}")

    if args.apply:
        args.topics_file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Arquivo atualizado: {args.topics_file}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
