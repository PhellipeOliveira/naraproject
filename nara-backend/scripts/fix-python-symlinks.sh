#!/bin/bash
# Remove symlinks do Python 3.14 e 3.13 (frameworks já removidos ou a remover)
# e faz python3 -> python3.12. Rodar com: sudo bash scripts/fix-python-symlinks.sh

set -e
BIN=/usr/local/bin

# Remover links 3.14 (e 3.14t)
for name in python3 python3-config python3-intel64 \
  python3.14 python3.14-config python3.14-intel64 \
  python3.14t python3.14t-config python3.14t-intel64 \
  python3t python3t-config python3t-intel64; do
  [ -L "$BIN/$name" ] && rm -f "$BIN/$name" && echo "Removed $BIN/$name"
done

# Remover links 3.13 (e 3.13t)
for name in python3.13 python3.13-config python3.13-intel64 \
  python3.13t python3.13t-config python3.13t-intel64; do
  [ -L "$BIN/$name" ] && rm -f "$BIN/$name" && echo "Removed $BIN/$name"
done

# Fazer python3 apontar para python3.12 (Homebrew)
if [ -x "$BIN/python3.12" ]; then
  ln -sf python3.12 "$BIN/python3"
  ln -sf python3.12-config "$BIN/python3-config"
  echo "Linked python3 -> python3.12"
fi

echo "Done. Run: python3 --version"
