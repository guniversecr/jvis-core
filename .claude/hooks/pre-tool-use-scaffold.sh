#!/bin/bash
# Pre-tool-use hook: Block file writes outside project directory
# Triggered on: Write, Edit tools
# Exit 0 = allow, Exit 2 = block

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.filePath // empty')

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
RESOLVED_PATH=$(cd "$(dirname "$FILE_PATH")" 2>/dev/null && pwd)/$(basename "$FILE_PATH") 2>/dev/null

# Allow writes to project directory
if [[ "$FILE_PATH" == "$PROJECT_DIR"* ]]; then
  exit 0
fi

# Allow writes to temp directories
if [[ "$FILE_PATH" == /tmp/* ]] || [[ "$FILE_PATH" == /var/folders/* ]] || [[ "$FILE_PATH" == "$TMPDIR"* ]]; then
  exit 0
fi

# Allow writes to home .claude directory (settings, memory, etc.)
if [[ "$FILE_PATH" == "$HOME/.claude"* ]]; then
  exit 0
fi

echo "Blocked: Write/Edit to path outside project directory: $FILE_PATH" >&2
echo "Allowed paths: $PROJECT_DIR/*, /tmp/*, \$HOME/.claude/*" >&2
exit 2
