# CI/CD Pipeline Templates

Ready-to-use pipeline configurations for various CI/CD platforms.

## Supported Platforms

| Platform | Directory | Status |
|----------|-----------|--------|
| GitHub Actions | `github-actions/` | Production |
| GitLab CI | `gitlab-ci/` | Production |
| Azure DevOps | `azure-devops/` | Production |
| AWS CodePipeline | `aws-codepipeline/` | Beta |
| Bitbucket Pipelines | `bitbucket/` | Beta |

## Stack-Specific Templates

Each platform has templates for different stacks:

### Python (FastAPI/Flask)
- Lint with Ruff
- Type check with MyPy
- Test with pytest
- Build Docker image
- Deploy to cloud

### Node.js (Express/React)
- Lint with ESLint
- Type check with TypeScript
- Test with Jest/Vitest
- Build application
- Deploy to cloud

### Rust (Axum)
- Lint with Clippy
- Format check with rustfmt
- Test with cargo test
- Build release binary
- Deploy to cloud

### Mobile (Expo/Kotlin/Swift)
- Lint and type check
- Run tests
- Build with EAS/Gradle/Xcode
- Deploy to stores

## Usage

### 1. Select Platform and Stack

```bash
jvis pipeline add github-actions python-fastapi
```

### 2. Customize Configuration

Edit the generated workflow file to match your project:
- Update environment variables
- Configure deployment targets
- Add secrets references

### 3. Commit and Push

```bash
git add .github/workflows/
git commit -m "ci: add CI/CD pipeline"
git push
```

## Environment Variables

All templates expect these secrets to be configured:

### AWS
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`

### Azure
- `AZURE_CREDENTIALS`
- `AZURE_SUBSCRIPTION_ID`

### GCP
- `GCP_CREDENTIALS`
- `GCP_PROJECT_ID`

### Docker Registry
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`
- `DOCKER_REGISTRY` (optional)
