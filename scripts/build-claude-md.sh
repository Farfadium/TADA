#!/bin/bash
# Build CLAUDE.md from instructions.md by replacing {{file}} includes recursively
# Usage: ./build-claude-md.sh

SYSTEM_DIR="$CLAUDE_PROJECT_DIR/_SYSTEM"

# Recursive function to process a file and resolve includes
# $1 = file path (relative to _SYSTEM)
process_file() {
    local file="$1"
    local dir=$(dirname "$file")

    while IFS= read -r line || [[ -n "$line" ]]; do
        if [[ "$line" =~ \{\{([^}]+)\}\} ]]; then
            # Extract the file path (relative to current file's directory)
            local include="${BASH_REMATCH[1]}"
            local include_path

            # Resolve path relative to current file's directory
            if [[ "$include" == /* ]]; then
                include_path="$include"
            else
                include_path="$dir/$include"
            fi

            # Normalize path (remove ./ and resolve ..)
            include_path=$(cd "$SYSTEM_DIR" && realpath --relative-to=. "$include_path" 2>/dev/null || echo "$include_path")

            if [[ -f "$SYSTEM_DIR/$include_path" ]]; then
                # Recursively process the included file
                process_file "$include_path"
            else
                echo "<!-- Include not found: $include_path -->"
            fi
        else
            echo "$line"
        fi
    done < "$SYSTEM_DIR/$file"
}

# Start processing from instructions.md
process_file "instructions.md" > "$CLAUDE_PROJECT_DIR/CLAUDE.md"
