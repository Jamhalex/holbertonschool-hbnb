#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIAGRAM_DIR="$ROOT_DIR/part1/diagrams"
OUT_DIR="$ROOT_DIR/part1/exports"
PUPPETEER_CFG="$ROOT_DIR/part1/puppeteer.json"

mkdir -p "$OUT_DIR"
rm -f "$OUT_DIR"/*.png

shopt -s nullglob
for f in "$DIAGRAM_DIR"/*.mmd; do
  base="$(basename "$f" .mmd)"
  npx mmdc -p "$PUPPETEER_CFG" -i "$f" -o "$OUT_DIR/${base}.png"
  echo "Rendered ${base}.png"
done
shopt -u nullglob

echo "PNG export complete: $OUT_DIR"
