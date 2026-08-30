#!/bin/sh
DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
if command -v xdg-open >/dev/null 2>&1; then xdg-open "$DIR/START.html"; elif command -v gio >/dev/null 2>&1; then gio open "$DIR/START.html"; elif command -v open >/dev/null 2>&1; then open "$DIR/START.html"; else echo "Open $DIR/START.html in a browser."; fi
