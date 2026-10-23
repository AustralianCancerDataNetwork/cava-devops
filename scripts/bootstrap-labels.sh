#!/usr/bin/env bash
# Apply the canonical CAVA label set to a GitHub repository.
# Usage: scripts/bootstrap-labels.sh <owner/repo>
# Requires: gh CLI, authenticated with repo write access.
set -euo pipefail

REPO="${1:-}"
if [[ -z "$REPO" ]]; then
  echo "Usage: $0 <owner/repo>"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LABELS_FILE="$SCRIPT_DIR/labels.yml"

# Parse labels.yml with Python (available everywhere uv is).
python3 - "$LABELS_FILE" "$REPO" <<'EOF'
import sys, subprocess
try:
    import yaml
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pyyaml"], check=True)
    import yaml

labels_file, repo = sys.argv[1], sys.argv[2]
with open(labels_file) as f:
    data = yaml.safe_load(f)

for label in data["labels"]:
    result = subprocess.run(
        ["gh", "label", "create", label["name"],
         "--repo", repo,
         "--color", label["color"],
         "--description", label["description"],
         "--force"],   # --force updates if it already exists
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"  OK  {label['name']}")
    else:
        print(f"  ERR {label['name']}: {result.stderr.strip()}")
EOF
