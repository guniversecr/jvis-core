#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

cd "$PROJECT_ROOT"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

fail() {
    echo -e "${RED}FAIL: $1${NC}"
    exit 1
}

pass() {
    echo -e "${GREEN}✓ $1${NC}"
}

echo "=== CLI Smoke Tests ==="

# Test 1: CLI is available (pip-installed entry point)
test_cli_exists() {
    command -v jvis >/dev/null 2>&1 || fail "jvis command not found (pip install -e . first)"
    pass "CLI command available"
}

# Test 2: CLI responds to --version
test_cli_version() {
    local version
    version=$(jvis version 2>/dev/null || jvis --version 2>/dev/null || echo "")
    [[ -n "$version" ]] || fail "CLI does not respond to version command"
    pass "CLI version: $version"
}

# Test 3: CLI responds to --help
test_cli_help() {
    local help_output
    help_output=$(jvis --help 2>&1)
    echo "$help_output" | grep -q "new" || fail "Help output incomplete"
    pass "CLI help works"
}

# Test 4: Version file exists
test_version_file() {
    [[ -f ".jvis/version" ]] || fail "Version file not found"
    local version
    version=$(cat .jvis/version)
    [[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || fail "Invalid version format: $version"
    pass "Version file valid: $version"
}

# Test 5: Core config exists
test_core_config() {
    [[ -f ".jvis/core-config.yaml" ]] || fail "core-config.yaml not found"
    pass "Core config exists"
}

# Test 6: Editions config exists
test_editions_config() {
    [[ -f ".jvis/editions.yaml" ]] || fail "editions.yaml not found"
    pass "Editions config exists"
}

# Run all tests
test_cli_exists
test_cli_version
test_cli_help
test_version_file
test_core_config
test_editions_config

echo ""
echo "=== CLI Smoke Tests PASSED ==="
