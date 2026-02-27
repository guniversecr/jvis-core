# Integration Project Workflow

Set up a project that integrates with external services.

## Workflow Overview

This workflow configures a project with external integrations:

1. **Scan Project** - Detect existing stack
2. **Detect Integrations** - Find integration patterns in code
3. **Generate Composition** - Create composition file
4. **Verify Agents** - Check required vs installed agents
5. **Install Missing** - Add missing agents
6. **Configure** - Set up integration configs
7. **Verify Setup** - Final verification

## Instructions

Execute the task defined in `.jvis/tasks/integration-project.md`.

### Detection Patterns

The workflow scans for these integrations:

| Integration | Python Pattern | JS/TS Pattern |
|-------------|---------------|---------------|
| Bitrix24 | `import bitrix24` | `@bitrix24/` |
| Shopify | `import shopify` | `@shopify/` |
| Odoo | `import odoorpc` | - |
| Amazon Connect | `boto3.*connect` | `ConnectClient` |
| AWS | `import boto3` | `@aws-sdk/` |
| Azure | `azure.*` | `@azure/` |

### Workflow Steps

```bash
# Step 1-2: Scan and detect
jvis composition detect .

# Step 3: Generate composition file
jvis composition generate .

# Step 4: Verify agents
jvis composition verify .

# Step 5: Install missing
jvis composition install .
```

### Manual Agent Addition

If automatic installation doesn't work:

```bash
# From JVIS directory, update the project
./update-project.sh /path/to/project

# Or copy specific agents
cp .claude/commands/bitrix.md /path/to/project/.claude/commands/
cp .claude/commands/connect.md /path/to/project/.claude/commands/
```

## Output

- `.jvis/project-composition.yaml` - Composition file
- All required agents installed
- Integration detection report

## Verification

After completion, verify with:

```bash
jvis composition verify .
```

Expected output:
```
All required agents are installed.
```

## Next Steps

Once setup is complete:
1. Load context: `*load-context` (will show composition)
2. Use integration agents as needed: `/bitrix`, `/connect`, etc.
3. Develop with full integration knowledge available
