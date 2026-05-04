#!/usr/bin/env zsh
set -e

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
CAPTURES="$REPO_ROOT/captures"
INDEX="$CAPTURES/index.json"

usage() {
    echo "Usage: post.sh <file> [caption]"
    echo "       Omit caption to be prompted interactively."
    exit 1
}

[ -z "$1" ] && usage
FILE="$1"
[ ! -f "$FILE" ] && { echo "File not found: $FILE"; exit 1; }

if [ -n "$2" ]; then
    CAPTION="$2"
else
    echo -n "Caption (leave blank to skip): "
    read CAPTION
fi

EXT="${FILE##*.}"
TIMESTAMP=$(date +"%Y-%m-%d-%H-%M-%S")
DEST_NAME="${TIMESTAMP}.${EXT}"
DEST="$CAPTURES/$DEST_NAME"

cp "$FILE" "$DEST"
echo "Copied → $DEST"

ISO_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
python3 - "$DEST_NAME" "$CAPTION" "$ISO_DATE" "$INDEX" <<'PYEOF'
import json, sys
name, caption, ts, index_path = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
entry = {"file": name, "caption": caption, "timestamp": ts}
try:
    with open(index_path) as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = []
data.insert(0, entry)
with open(index_path, "w") as f:
    json.dump(data, f, indent=2)
print(f"Index updated ({len(data)} entries)")
PYEOF

cd "$REPO_ROOT"
git add "captures/$DEST_NAME" "$INDEX"
git commit -m "${CAPTION:-Gamedev update $TIMESTAMP}"
git push

rm "$DEST"
echo "Pushed and cleaned up local copy. GitHub Actions will upload to releases, post to socials, and update the gallery."
