#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "=== JVIS Test Suite ==="
echo ""

# Smoke tests
echo "--- Smoke Tests ---"
for test in tests/smoke/test_*.sh; do
    if [[ -x "$test" ]]; then
        echo "Running: $test"
        bash "$test" || { echo "FAILED: $test"; exit 1; }
    fi
done

echo ""
echo "=== All Tests PASSED ==="
