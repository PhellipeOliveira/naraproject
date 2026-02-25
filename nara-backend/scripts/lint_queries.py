"""
Linter para detectar queries RAG condensadas, longas e redundantes.

Uso:
  python -m scripts.lint_queries
  python -m scripts.lint_queries --json
  python -m scripts.lint_queries --json reports/lint_report.json
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
    parser = argparse.ArgumentParser(description="Lint de queries do rag_coverage_topics.json")
    parser.add_argument(
        "--topics-file",
        type=Path,
        default=backend_root / "scripts" / "rag_coverage_topics.json",
        help="Arquivo JSON de topicos (default: scripts/rag_coverage_topics.json)",
    )
    parser.add_argument(
        "--json",
        nargs="?",
        const="lint_report.json",
        default=None,
        metavar="OUTPUT",
        help="Grava relatorio JSON (default quando omitido: lint_report.json)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=10,
        help="Limite de tokens para flag de query longa (default: 10)",
    )
    parser.add_argument(
        "--max-group-queries",
        type=int,
        default=20,
        help="Alerta de explosao de queries por grupo (default: 20)",
    )
    parser.add_argument(
        "--redundancy-distance-threshold",
        type=float,
        default=0.3,
        help="Threshold da distancia de Jaccard para redundancia (default: 0.3)",
    )
    return parser.parse_args()


def load_topics(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Arquivo de topicos nao encontrado: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    groups = data.get("groups")
    if not isinstance(data, dict) or not isinstance(groups, list):
        raise ValueError("Formato invalido: esperado objeto JSON com lista em 'groups'.")
    return data


def normalize_text(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value)
    without_accents = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    lowered = without_accents.lower()
    cleaned = re.sub(r"[^a-z0-9+\s]", " ", lowered)
    return re.sub(r"\s+", " ", cleaned).strip()


def tokenize(value: str) -> list[str]:
    norm = normalize_text(value)
    if not norm:
        return []
    return norm.split(" ")


def contains_phrase(text: str, phrase: str) -> bool:
    if not phrase:
        return False
    return f" {phrase} " in f" {text} "


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


def detect_concepts_in_query(query: str, concepts: list[str]) -> list[str]:
    norm_query = normalize_text(query)
    detected: list[str] = []
    for concept in concepts:
        for alias in concept_aliases(str(concept)):
            alias_norm = normalize_text(alias)
            if alias_norm and contains_phrase(norm_query, alias_norm):
                detected.append(str(concept))
                break
    return detected


def jaccard_distance(query_a: str, query_b: str) -> float:
    set_a = set(tokenize(query_a))
    set_b = set(tokenize(query_b))
    if not set_a and not set_b:
        return 0.0
    union = set_a | set_b
    if not union:
        return 0.0
    similarity = len(set_a & set_b) / len(union)
    return 1.0 - similarity


def is_prefix_relation(query_a: str, query_b: str) -> bool:
    a = normalize_text(query_a)
    b = normalize_text(query_b)
    return a.startswith(b + " ") or b.startswith(a + " ")


def domain_markers(query: str) -> set[str]:
    return set(re.findall(r"\bd\d+\b", normalize_text(query)))


def strip_detected_concepts(query: str, detected_concepts: list[str]) -> str:
    root = query
    for concept in detected_concepts:
        pattern = re.compile(re.escape(concept), flags=re.IGNORECASE)
        root = pattern.sub(" ", root)
    return re.sub(r"\s+", " ", root).strip()


def suggest_split(query: str, group_title: str, detected_concepts: list[str]) -> list[str]:
    if len(detected_concepts) < 2:
        return []

    root = strip_detected_concepts(query, detected_concepts)
    if not root:
        root = re.sub(r"^\d+\s+", "", group_title).strip()
        root = root.lower()

    suggestions: list[str] = []
    if root:
        suggestions.append(root)
    for concept in detected_concepts:
        candidate = f"{root} {concept}".strip() if root else concept
        suggestions.append(candidate)

    dedup: list[str] = []
    seen: set[str] = set()
    for item in suggestions:
        norm = normalize_text(item)
        if norm and norm not in seen:
            dedup.append(item)
            seen.add(norm)
    return dedup


def build_lint_report(
    topics_data: dict[str, Any],
    max_tokens: int,
    max_group_queries: int,
    redundancy_distance_threshold: float,
) -> dict[str, Any]:
    groups = topics_data["groups"]
    findings: list[dict[str, Any]] = []

    connectors = {"e", "ou", "de", "da", "do", "dos", "das", "com", "para", "por", "em", "na", "no", "nas", "nos"}
    verbs = {
        "validar",
        "regular",
        "ressignificar",
        "reconhecer",
        "modelar",
        "assumir",
        "reforcar",
        "diagnosticar",
        "estruturar",
        "analisar",
        "transformar",
    }

    for group in groups:
        group_id = str(group.get("id", "unknown"))
        group_title = str(group.get("title", group_id))
        concepts = [str(c) for c in (group.get("concepts") or [])]
        queries = [str(q) for q in (group.get("queries") or [])]
        concept_norm_tokens = {normalize_text(c) for c in concepts}

        if len(queries) > max_group_queries:
            findings.append(
                {
                    "group_id": group_id,
                    "group_title": group_title,
                    "query": "",
                    "flags": ["query_explosion"],
                    "details": {
                        "total_queries": len(queries),
                        "max_group_queries": max_group_queries,
                    },
                    "suggested_action": "review",
                    "suggestions": [],
                }
            )

        redundant_pairs: dict[int, list[dict[str, Any]]] = {}
        for i in range(len(queries)):
            for j in range(i + 1, len(queries)):
                tokens_i = tokenize(queries[i])
                tokens_j = tokenize(queries[j])
                if len(tokens_i) < 5 or len(tokens_j) < 5:
                    continue
                if is_prefix_relation(queries[i], queries[j]):
                    continue
                markers_i = domain_markers(queries[i])
                markers_j = domain_markers(queries[j])
                if markers_i and markers_j and markers_i != markers_j:
                    continue
                distance = jaccard_distance(queries[i], queries[j])
                if distance < redundancy_distance_threshold:
                    redundant_pairs.setdefault(i, []).append({"other_index": j, "distance": round(distance, 4)})
                    redundant_pairs.setdefault(j, []).append({"other_index": i, "distance": round(distance, 4)})

        for idx, query in enumerate(queries):
            flags: list[str] = []
            details: dict[str, Any] = {}

            query_tokens = tokenize(query)
            detected_concepts = detect_concepts_in_query(query, concepts)

            if len(detected_concepts) >= 2:
                flags.append("condensada")
                details["detected_concepts"] = detected_concepts

            if len(query_tokens) > max_tokens:
                flags.append("longa")
                details["token_count"] = len(query_tokens)
                details["max_tokens"] = max_tokens

            concept_token_hits = sum(1 for token in query_tokens if token in concept_norm_tokens)
            has_connector = any(token in connectors for token in query_tokens)
            has_verb = any(token in verbs for token in query_tokens)
            if concept_token_hits >= 3 and not has_connector and not has_verb:
                flags.append("lista_seca")
                details["concept_token_hits"] = concept_token_hits

            if idx in redundant_pairs:
                flags.append("redundante")
                details["redundant_with"] = redundant_pairs[idx]

            if not flags:
                continue

            suggested_action = "keep"
            suggestions: list[str] = []
            if "condensada" in flags:
                suggested_action = "split"
                suggestions = suggest_split(query, group_title, detected_concepts)
            elif "redundante" in flags:
                suggested_action = "dedupe"

            findings.append(
                {
                    "group_id": group_id,
                    "group_title": group_title,
                    "query_index": idx,
                    "query": query,
                    "flags": flags,
                    "details": details,
                    "suggested_action": suggested_action,
                    "suggestions": suggestions,
                }
            )

    return {
        "topics_file": str(topics_data.get("source", "")),
        "total_findings": len(findings),
        "findings": findings,
    }


def print_report(report: dict[str, Any]) -> None:
    findings = report["findings"]
    if not findings:
        print("Nenhuma query suspeita encontrada.")
        return

    print(f"Total de findings: {len(findings)}")
    print("")
    for item in findings:
        group = item["group_id"]
        query = item.get("query", "")
        flags = ", ".join(item["flags"])
        action = item["suggested_action"]
        print(f"[{group}] flags={flags} action={action}")
        if query:
            print(f"  query: {query}")
        suggestions = item.get("suggestions") or []
        if suggestions:
            print("  sugestoes:")
            for s in suggestions:
                print(f"   - {s}")
        print("")


def main() -> int:
    args = parse_args()
    topics_data = load_topics(args.topics_file)
    report = build_lint_report(
        topics_data=topics_data,
        max_tokens=args.max_tokens,
        max_group_queries=args.max_group_queries,
        redundancy_distance_threshold=args.redundancy_distance_threshold,
    )

    print_report(report)

    if args.json is not None:
        output_path = Path(args.json)
        output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Relatorio JSON salvo em: {output_path}")

    blocking_flags = {"condensada", "redundante"}
    blocking_count = 0
    for item in report["findings"]:
        if any(flag in blocking_flags for flag in item["flags"]):
            blocking_count += 1

    if blocking_count:
        print(f"Findings bloqueantes: {blocking_count}")
    return 1 if blocking_count > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
