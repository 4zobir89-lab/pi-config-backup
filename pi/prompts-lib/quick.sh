#!/bin/bash
# Quick prompts.chat search
# Usage: quick.sh "search term"

QUERY="${1:-}"
if [ -z "$QUERY" ]; then
    echo "Usage: quick.sh \"search term\""
    echo "Example: quick.sh \"linux\""
    exit 1
fi

python3 /root/.pi/prompts-lib/query.py search "$QUERY"
