# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 4.x     | Yes                |
| < 4.0   | No                 |

Only the latest release receives security updates.

## Reporting a Vulnerability

**Do not open a public issue for security vulnerabilities.**

Use [GitHub Private Vulnerability Reporting](https://github.com/guniversecr/jvis/security/advisories/new) to report security issues.

### What to include

- Description of the vulnerability
- Steps to reproduce
- Affected versions
- Impact assessment (if known)

### Response timeline

- **Acknowledgment:** within 48 hours
- **Initial assessment:** within 7 days
- **Fix or mitigation:** depends on severity, targeting 30 days for critical issues

### What qualifies as a vulnerability

- Code injection via agent configs or templates
- Path traversal in `jvis new` / `jvis add` / `jvis update`
- Credential exposure in generated files
- Supply chain issues in dependencies
- MCP server vulnerabilities that could affect host systems

### What does NOT qualify

- Bugs that require local admin access to exploit
- Issues in draft/config-template agents (48 agents with no tested workflows)
- Cosmetic issues in generated documentation
- Feature requests

## Security Measures

This project uses:
- OIDC trusted publishing for PyPI (no stored API tokens)
- GitHub Actions pinned to commit SHAs
- Bandit SAST scanning on all PRs
- TruffleHog secret scanning on all PRs
- Dependabot for dependency updates
- Pre-commit hooks for local secret detection
