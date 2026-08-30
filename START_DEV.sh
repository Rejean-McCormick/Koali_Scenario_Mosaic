#!/bin/sh
set -e
DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$DIR"
if ! command -v npm >/dev/null 2>&1; then echo "Node.js/npm is required for development. Use START.html for the zero-install preview."; exit 1; fi
[ -d node_modules ] || npm install
npm run dev -- --open /uses/
