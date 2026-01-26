#!/bin/bash
# Build CLAUDE.md from instructions.md by replacing {{file}} includes
# Usage: ./build-claude-md.sh

cd "$CLAUDE_PROJECT_DIR/_SYSTEM"

# Process the source file line by line
while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ "$line" =~ \{\{([^}]+)\}\} ]]; then
        # Extract the file path and include its content
        filepath="${BASH_REMATCH[1]}"
        if [[ -f "$filepath" ]]; then
            cat "$filepath"
        else
            echo "<!-- Include not found: $filepath -->"
        fi
    else
        echo "$line"
    fi
done < instructions.md > ../CLAUDE.md
