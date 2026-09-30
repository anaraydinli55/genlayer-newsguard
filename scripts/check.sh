#!/usr/bin/env bash
# Reproducible check. Prerequisites: python3 + pytest (see requirements-dev.txt), node, `npm ci` in ./frontend
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== 1. SDK pin =="
head -1 NewsGuard.py | grep -Eq 'py-genlayer:[0-9a-z]{40,}' || { echo "py-genlayer runner is not pinned by hash"; exit 1; }
node -e '
const r = require("./package.json").dependencies["genlayer-js"];
const f = require("./frontend/package.json").dependencies["genlayer-js"];
if (!/^\d+\.\d+\.\d+$/.test(r) || r !== f) { console.error("genlayer-js must be one exact version in both package.json files:", r, f); process.exit(1); }
console.log("genlayer-js", r);
'

echo "== 2. contract syntax =="
python3 -m py_compile NewsGuard.py

echo "== 3. contract tests =="
python3 -m pytest tests -q

echo "== 4. frontend types =="
(cd frontend && npx tsc --noEmit)

echo "ALL CHECKS PASSED"
