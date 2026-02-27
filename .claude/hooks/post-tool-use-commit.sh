#!/bin/bash
# Post-tool-use hook: Validate conventional commit format
# Triggered on: Bash tool (after git commit)
# Exit 0 = ok, Exit 2 = block (but post-tool, so just warn)

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Only check git commit commands
if ! echo "$COMMAND" | grep -q 'git commit' 2>/dev/null; then
  exit 0
fi

# Extract commit message from -m flag (POSIX-compatible, no grep -P)
COMMIT_MSG=$(echo "$COMMAND" | sed -n 's/.*-m[[:space:]]*["'"'"']\([^"'"'"']*\)["'"'"'].*/\1/p' 2>/dev/null)

# Also try heredoc pattern: -m "$(cat <<'EOF' ... EOF )"
if [ -z "$COMMIT_MSG" ]; then
  COMMIT_MSG=$(echo "$COMMAND" | sed -n 's/.*-m[[:space:]]*"\$(cat <<.*//p' 2>/dev/null)
  if [ -n "$COMMIT_MSG" ]; then
    # For heredoc, extract the first content line after EOF marker
    COMMIT_MSG=$(echo "$COMMAND" | sed -n '/EOF$/,/EOF/{/EOF/d;p;}' 2>/dev/null | head -1 | sed 's/^[[:space:]]*//')
  fi
fi

# If we couldn't extract the message, allow it (might be interactive or complex)
if [ -z "$COMMIT_MSG" ]; then
  exit 0
fi

# Get first line of commit message
FIRST_LINE=$(echo "$COMMIT_MSG" | head -1)

# Validate conventional commit format: type: description
# Valid types: feat, fix, refactor, test, docs, chore, ci, build, perf, style
if echo "$FIRST_LINE" | grep -qE '^(feat|fix|refactor|test|docs|chore|ci|build|perf|style)(\(.+\))?: .+'; then
  exit 0
fi

echo "Warning: Commit message does not follow conventional format." >&2
echo "Expected: type: description (e.g., 'feat: add user auth')" >&2
echo "Valid types: feat, fix, refactor, test, docs, chore, ci, build, perf, style" >&2
echo "Got: $FIRST_LINE" >&2
exit 0
