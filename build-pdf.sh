#!/usr/bin/env bash
set -euo pipefail
project_dir="$(cd "$(dirname "$0")" && pwd)"
chromium --headless --no-sandbox --disable-gpu --print-to-pdf="$project_dir/portfolio-ermirio-bonfim.pdf" --print-to-pdf-no-header "file://$project_dir/index.html"
echo "PDF criado em $project_dir/portfolio-ermirio-bonfim.pdf"
