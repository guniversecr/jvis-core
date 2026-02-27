#!/bin/bash
# Pre-tool-use hook: Block production database connections in test files
# Triggered on: Write, Edit tools
# Exit 0 = allow, Exit 2 = block

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.filePath // empty')
CONTENT=$(echo "$INPUT" | jq -r '.tool_input.content // .tool_input.new_string // empty')

if [ -z "$FILE_PATH" ] || [ -z "$CONTENT" ]; then
  exit 0
fi

# Only check test files
if [[ "$FILE_PATH" != *test* ]] && [[ "$FILE_PATH" != *spec* ]] && [[ "$FILE_PATH" != *tests/* ]]; then
  exit 0
fi

# Block production database connection strings (allow SQLite and in-memory)
if echo "$CONTENT" | grep -qiE '(postgresql://|mysql://|mongodb://|redis://|postgres://)' 2>/dev/null; then
  # Allow if it's clearly a test/mock connection
  if echo "$CONTENT" | grep -qiE '(localhost|127\.0\.0\.1|mock|fake|test_db|:memory:)' 2>/dev/null; then
    exit 0
  fi
  echo "Blocked: Production database connection string detected in test file: $FILE_PATH" >&2
  echo "Use SQLite/:memory: or localhost connections for tests." >&2
  exit 2
fi

exit 0
