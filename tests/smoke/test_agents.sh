#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

cd "$PROJECT_ROOT"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

fail() {
    echo -e "${RED}FAIL: $1${NC}"
    exit 1
}

pass() {
    echo -e "${GREEN}✓ $1${NC}"
}

warn() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

echo "=== Agent Smoke Tests ==="

# Test 1: Agents directory exists
test_agents_dir() {
    [[ -d ".jvis/agents" ]] || fail "Agents directory not found"
    pass "Agents directory exists"
}

# Test 2: Minimum number of agents (YAML configs)
test_agent_count() {
    local count
    count=$(find .jvis/agents -name "*.yaml" -type f | wc -l | tr -d ' ')
    [[ $count -ge 15 ]] || fail "Expected at least 15 agents, found $count"
    pass "$count agent configs found"
}

# Test 3: Agent YAML files have required fields
test_agent_yaml_structure() {
    local errors=0
    for agent in $(find .jvis/agents -name "*.yaml" -type f); do
        # Check for id field (top-level, no indentation)
        if ! grep -q '^id:' "$agent" 2>/dev/null; then
            warn "Missing 'id:' in $(basename "$agent")"
            ((errors++)) || true
        fi

        # Check for name field
        if ! grep -q '^name:' "$agent" 2>/dev/null; then
            warn "Missing 'name:' in $(basename "$agent")"
            ((errors++)) || true
        fi
    done

    [[ $errors -eq 0 ]] || fail "$errors agents have structure issues"
    pass "All agent YAML files have valid structure"
}

# Test 4: Agents have unique IDs
test_agent_unique_ids() {
    local ids
    ids=$(grep -rh '^id: ' .jvis/agents/ --include="*.yaml" 2>/dev/null | sed 's/.*id:\s*//' | sed "s/['\"]//g" | sort)
    local total
    total=$(echo "$ids" | grep -c . || echo 0)
    local unique
    unique=$(echo "$ids" | sort -u | grep -c . || echo 0)

    [[ "$total" -eq "$unique" ]] || fail "Duplicate agent IDs found ($total vs $unique unique)"
    pass "All agent IDs are unique ($unique agents)"
}

# Test 5: Commands directory has slash commands
test_commands_exist() {
    local command_count
    command_count=$(find .claude/commands -name "*.md" -type f | grep -v README | grep -v workflows | wc -l | tr -d ' ')
    [[ $command_count -ge 10 ]] || fail "Too few commands: $command_count"
    pass "$command_count slash commands found"
}

# Run all tests
test_agents_dir
test_agent_count
test_agent_yaml_structure
test_agent_unique_ids
test_commands_exist

echo ""
echo "=== Agent Smoke Tests PASSED ==="
