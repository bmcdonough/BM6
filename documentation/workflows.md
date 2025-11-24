# GitHub Workflows Documentation

This document provides detailed explanations of all GitHub Actions workflows used in the BM6 project.

## Overview

The BM6 project uses four primary workflows to ensure code quality, validate Home Assistant integration standards, and automate the release process. All workflows are located in `.github/workflows/`.

---

## CodeQL Advanced (`codeql.yml`)

**Purpose:** Automated security vulnerability scanning and code quality analysis.

**File:** `.github/workflows/codeql.yml`

### Triggers
- **Push to main branch** - Scans code on every push to main
- **Pull requests to main branch** - Validates PRs before merging
- **Scheduled** - Runs weekly on Fridays at 21:44 UTC (`cron: '44 21 * * 5'`)

### What It Does
CodeQL is GitHub's semantic code analysis engine that:
- Analyzes Python code for security vulnerabilities
- Detects common coding errors and bugs
- Identifies potential security issues (SQL injection, XSS, etc.)
- Provides detailed findings in GitHub Security tab

### Configuration
- **Language:** Python only (can be extended to support other languages)
- **Runner:** Ubuntu-latest (macOS-latest for Swift if added)
- **Permissions:**
  - `security-events: write` - Upload scan results
  - `packages: read` - Access CodeQL packs
  - `actions: read` - Read workflow data
  - `contents: read` - Checkout repository

### Workflow Steps
1. Checkout repository
2. Initialize CodeQL tools for Python
3. Perform automated analysis
4. Upload results to GitHub Security

### Notes
- Results appear in the repository's Security > Code scanning alerts
- Can be customized with custom queries for project-specific security requirements
- Analysis time depends on codebase size

---

## HACS Validation (`hacs.yaml`)

**Purpose:** Validates integration meets Home Assistant Community Store (HACS) requirements.

**File:** `.github/workflows/hacs.yaml`

### Triggers
- **Push to main branch** - Validates on every main branch push
- **Pull requests to main branch** - Ensures PRs meet HACS standards
- **Scheduled** - Runs daily at midnight UTC (`cron: "0 0 * * *"`)
- **Manual trigger** - Can be run on-demand via `workflow_dispatch`

### What It Does
HACS validation ensures the integration:
- Has proper repository structure
- Includes required metadata files (manifest.json, etc.)
- Follows HACS naming conventions
- Contains valid integration configuration
- Meets HACS distribution requirements

### Configuration
- **Category:** Integration (as opposed to theme, plugin, etc.)
- **Runner:** Ubuntu-latest
- **Action:** Uses official `hacs/action@main`

### Workflow Steps
1. Checkout repository with full history
2. Run HACS validation action
3. Report validation results

### Notes
- HACS is the most popular way to distribute custom Home Assistant integrations
- Validation failures will block merges if set as required check
- Daily runs help catch issues from upstream changes

---

## Hassfest Validation (`hassfest.yaml`)

**Purpose:** Validates integration meets official Home Assistant integration standards.

**File:** `.github/workflows/hassfest.yaml`

### Triggers
- **Push to main branch** - Validates on every main branch push
- **Pull requests to main branch** - Ensures PRs meet Home Assistant standards
- **Scheduled** - Runs daily at midnight UTC (`cron: "0 0 * * *"`)
- **Manual trigger** - Can be run on-demand via `workflow_dispatch`

### What It Does
Hassfest is Home Assistant's official validation tool that checks:
- **manifest.json** - Valid structure, required fields, version format
- **strings.json** - Translation file validation
- **services.yaml** - Service definitions
- **Dependencies** - Required Python packages
- **Code quality** - Integration follows Home Assistant guidelines
- **Documentation** - Required documentation present

### Configuration
- **Runner:** Ubuntu-latest
- **Action:** Uses official `home-assistant/actions/hassfest@master`

### Workflow Steps
1. Checkout repository with full history
2. Run hassfest validation action
3. Report validation results

### Notes
- More comprehensive than HACS validation
- Required for official Home Assistant integration inclusion
- Daily runs catch breaking changes from Home Assistant core updates
- Validation results appear in workflow logs

---

## Release (`release.yml`)

**Purpose:** Automates the creation and publishing of integration releases.

**File:** `.github/workflows/release.yml`

### Triggers
- **Release published** - Runs when a new GitHub release is created and published

### What It Does
Automates the complete release process:
1. **Version Management** - Updates version numbers in code
2. **Packaging** - Creates distribution ZIP file
3. **Signing** - Cryptographically signs the release package
4. **Publishing** - Uploads signed package to GitHub release

### Configuration
- **Runner:** Ubuntu-latest
- **Permissions:**
  - `contents: write` - Upload release assets
  - `id-token: write` - Sign packages with sigstore
- **Environment Variable:**
  - `BM6_ROOT_DIR` - Points to `custom_components/bm6`

### Workflow Steps

#### 1. Checkout Repository
Uses `actions/checkout@v4.2.1` to get the code

#### 2. Adjust Version Numbers
- Extracts version from release tag (e.g., `v1.2.3` → `1.2.3`)
- Converts to lowercase and removes 'v' prefix
- Updates version in:
  - `custom_components/bm6/const.py` - Python constant
  - `custom_components/bm6/manifest.json` - Integration manifest

#### 3. Create ZIP Package
- Changes to integration directory
- Creates `bm6.zip` containing all integration files
- Preserves directory structure for Home Assistant

#### 4. Sign Package
- Uses `sigstore/gh-action-sigstore-python@v3.0.0`
- Creates cryptographic signature for verification
- Provides tamper-proof verification for users

#### 5. Upload to Release
- Uses `softprops/action-gh-release@v2.2.1`
- Attaches `bm6.zip` to the GitHub release
- Makes package available for download

### Notes
- Only runs when release is published (not draft releases)
- Version number is automatically synced from git tag
- Sigstore provides keyless code signing (no need to manage keys)
- ZIP file structure matches Home Assistant's expected format
- Users can verify package authenticity using sigstore signatures

### Release Process for Maintainers
1. Create new release on GitHub with version tag (e.g., `v1.2.3`)
2. Publish the release (not draft)
3. Workflow automatically:
   - Updates version numbers
   - Creates and signs package
   - Uploads to release
4. Users can download signed `bm6.zip` from release page

---

## Workflow Best Practices

### Local Testing
Before pushing changes:
- Validate manifest.json structure
- Test integration in Home Assistant
- Run local linters if available

### Required Checks
Consider making these workflows required for PR merges:
- HACS validation
- Hassfest validation
- CodeQL (for security)

### Monitoring
- Review CodeQL security alerts regularly
- Check workflow runs after dependency updates
- Monitor for upstream changes in Home Assistant

### Troubleshooting
- Check workflow logs in Actions tab
- Review specific step failures
- Consult linked documentation for validation errors

---

## Related Links

- [HACS Documentation](https://hacs.xyz/)
- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [CodeQL Documentation](https://codeql.github.com/)
- [Sigstore Documentation](https://www.sigstore.dev/)
