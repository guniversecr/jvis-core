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

echo "=== Template Smoke Tests ==="

# Test 1: Templates directory exists
test_templates_dir() {
    [[ -d ".jvis/templates" ]] || fail "Templates directory not found"
    pass "Templates directory exists"
}

# Test 2: Minimum number of templates
test_template_count() {
    local count
    count=$(find .jvis/templates -type f \( -name "*-tmpl.*" -o -name "*-tmpl" -o -name "*.tmpl.*" \) | wc -l | tr -d ' ')
    [[ $count -ge 80 ]] || fail "Expected at least 80 templates, found $count"
    pass "$count templates found"
}

# Test 3: Template subdirectories exist
test_template_categories() {
    local subdir_count
    subdir_count=$(find .jvis/templates -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
    [[ $subdir_count -ge 3 ]] || fail "Expected at least 3 template subdirectories, found $subdir_count"
    pass "$subdir_count template subdirectories found"
}

# Test 4: YAML config files are valid (skip templates — they embed markdown/Jinja2)
test_yaml_configs_valid() {
    local errors=0
    while IFS= read -r -d '' config; do
        if ! python3 -c "import yaml; yaml.safe_load(open('$config'))" 2>/dev/null; then
            echo "  Invalid YAML: $config"
            ((errors++)) || true
        fi
    done < <(find .jvis/agents .jvis/agent-engine/schemas -name "*.yaml" -print0 2>/dev/null)

    [[ $errors -eq 0 ]] || fail "$errors YAML configs are invalid"
    pass "All YAML config files are valid"
}

# Test 5: No empty templates
test_no_empty_templates() {
    local empty=0
    while IFS= read -r -d '' template; do
        if [[ ! -s "$template" ]]; then
            echo "  Empty: $template"
            ((empty++)) || true
        fi
    done < <(find .jvis/templates -type f -name "*-tmpl*" -print0 2>/dev/null)

    [[ $empty -eq 0 ]] || fail "$empty templates are empty"
    pass "No empty templates"
}

# Run all tests
test_templates_dir
test_template_count
test_template_categories
test_yaml_configs_valid
test_no_empty_templates

echo ""
echo "=== Template Smoke Tests PASSED ==="
