# BM6 Release Process

This document provides step-by-step instructions for creating a new release of the BM6 Home Assistant integration.

## Overview

The BM6 project uses an automated release workflow that handles:
- Version number synchronization
- Package creation and compression
- Cryptographic signing with Sigstore
- Asset uploading to GitHub releases

As a maintainer, you only need to prepare the release and create the GitHub release tag. The automation handles the rest.

---

## Table of Contents

1. [Pre-Release Checklist](#pre-release-checklist)
2. [Version Number Guidelines](#version-number-guidelines)
3. [Step-by-Step Release Process](#step-by-step-release-process)
4. [What the Automation Does](#what-the-automation-does)
5. [Post-Release Tasks](#post-release-tasks)
6. [Troubleshooting](#troubleshooting)
7. [Hotfix Releases](#hotfix-releases)
8. [Rolling Back a Release](#rolling-back-a-release)

---

## Pre-Release Checklist

Before creating a release, ensure all of the following are complete:

### 1. Code Quality

- [ ] All tests pass locally
  ```bash
  pytest tests/
  ```

- [ ] Code passes all linters
  ```bash
  python3 -m pylint custom_components/bm6/
  ruff check custom_components/bm6/
  ```

- [ ] No obvious bugs or issues in the code
- [ ] Code review completed (if working with a team)

### 2. Validation Workflows

- [ ] GitHub Actions workflows all passing:
  - CodeQL security scan (green check)
  - HACS validation (green check)
  - Hassfest validation (green check)

- [ ] Check workflow status:
  ```bash
  # Or visit: https://github.com/YOUR_USERNAME/BM6/actions
  gh workflow list
  gh run list --limit 5
  ```

### 3. Integration Testing

- [ ] Test the integration in a real Home Assistant instance:
  ```bash
  # Start Home Assistant with dev config
  hass -c config/
  ```

- [ ] Verify all features work:
  - [ ] Integration can be added via UI
  - [ ] Device discovery works
  - [ ] All sensors report correct values
  - [ ] Configuration options work
  - [ ] No errors in logs

- [ ] Test on multiple platforms if possible:
  - [ ] Home Assistant Core
  - [ ] Home Assistant Container
  - [ ] Home Assistant OS

### 4. Documentation

- [ ] README.md is up-to-date
- [ ] CHANGELOG.md is updated with new version
- [ ] All documentation reflects current features
- [ ] Screenshots/examples are current

### 5. Dependencies

- [ ] All dependencies are pinned in `manifest.json` (if any)
- [ ] No deprecated dependencies
- [ ] Dependencies compatible with target Home Assistant version
- [ ] Check minimum Home Assistant version in `const.py`:
  ```python
  MIN_REQUIRED_HA_VERSION = "2025.1.1"
  ```

### 6. Version Compatibility

- [ ] Test against minimum supported Home Assistant version
- [ ] Test against latest Home Assistant stable version
- [ ] Update `MIN_REQUIRED_HA_VERSION` if necessary

### 7. Security

- [ ] No hardcoded secrets or credentials
- [ ] No sensitive data in logs (even debug logs)
- [ ] CodeQL scan shows no high-severity issues
- [ ] Dependencies have no known critical vulnerabilities

---

## Version Number Guidelines

BM6 uses [Semantic Versioning](https://semver.org/): **MAJOR.MINOR.PATCH**

### Version Format: `X.Y.Z`

- **MAJOR (X)** - Incompatible API changes or major breaking changes
  - Example: `1.0.3` → `2.0.0`
  - Requires users to reconfigure or significant migration
  - Reserved for major architecture changes

- **MINOR (Y)** - New features, backwards-compatible
  - Example: `1.0.3` → `1.1.0`
  - Adds new sensors, features, or configuration options
  - Existing configurations continue to work

- **PATCH (Z)** - Bug fixes, backwards-compatible
  - Example: `1.0.3` → `1.0.4`
  - Fixes bugs, improves reliability
  - No new features, no breaking changes

### Examples

**PATCH Release (1.0.3 → 1.0.4):**
- Fixed temperature sensor returning null
- Corrected battery percentage calculation
- Fixed memory leak in Bluetooth connection
- Updated translation strings

**MINOR Release (1.0.3 → 1.1.0):**
- Added support for new BM6 device model
- Added new "battery health" sensor
- Added support for multiple Bluetooth scanners
- Improved performance for data updates

**MAJOR Release (1.0.3 → 2.0.0):**
- Complete rewrite of Bluetooth communication
- Changed configuration format (requires reconfiguration)
- Removed deprecated sensors
- Changed entity IDs (breaking change for automations)

### Deciding the Version Number

Ask yourself:
1. **Does this break existing setups?** → MAJOR bump
2. **Does this add new features?** → MINOR bump
3. **Does this only fix bugs?** → PATCH bump

When in doubt, start with a PATCH or MINOR release. MAJOR releases should be rare and well-documented.

---

## Step-by-Step Release Process

Follow these steps to create a new release:

### Step 1: Ensure You're on Main Branch

```bash
# Check current branch
git branch

# Switch to main if needed
git checkout main

# Pull latest changes
git pull origin main
```

**Verify you're on the correct branch:**
- Branch should be `main` (not `dev` or feature branch)
- Working directory should be clean (no uncommitted changes)

### Step 2: Update Version Numbers

Update the version in **both** of these files:

#### File 1: `custom_components/bm6/const.py`

```python
VERSION = "1.0.4"  # Update this line
```

Find line 9 and update the version string.

#### File 2: `custom_components/bm6/manifest.json`

```json
{
  "version": "1.0.4"
}
```

Find line 54 and update the version string.

**Important:** Both files must have the **exact same version number**.

#### Commands:
```bash
# Edit const.py
# Find: VERSION = "1.0.3"
# Replace with: VERSION = "1.0.4"

# Edit manifest.json
# Find: "version": "1.0.3"
# Replace with: "version": "1.0.4"

# Verify the changes
grep -n "VERSION = " custom_components/bm6/const.py
grep -n '"version"' custom_components/bm6/manifest.json
```

### Step 3: Update CHANGELOG.md

Add release notes for the new version at the top of `CHANGELOG.md`, right after the `<!--next-version-placeholder-->` comment.

**Format:**
```markdown
# Changelog

<!--next-version-placeholder-->

## 1.0.4
- Fixed bug in battery percentage calculation
- Improved Bluetooth connection stability
- Updated Polish translations

## 1.0.3
- Added support for multiple Bluetooth scanners/gateways...
```

**Guidelines:**
- Use clear, user-focused descriptions
- Start each item with a verb (Added, Fixed, Improved, Updated, Removed)
- Group similar changes together
- Highlight breaking changes clearly
- Be specific but concise

**Example Entries:**
```markdown
## 1.1.0
- Added support for BM6 Pro device model
- Added new "Battery Health" sensor showing battery condition
- Improved error messages for connection failures
- Updated German and French translations
- Fixed issue where temperature sensor would occasionally return null
- **Breaking:** Renamed `battery_state` sensor to `charge_state` for clarity

## 1.0.4
- Fixed memory leak in Bluetooth connection handler
- Fixed incorrect battery percentage when voltage is near maximum
- Improved reconnection logic after Home Assistant restart
- Updated minimum Home Assistant version to 2025.1.1
```

### Step 4: Commit Version Changes

```bash
# Add the modified files
git add custom_components/bm6/const.py
git add custom_components/bm6/manifest.json
git add CHANGELOG.md

# Commit with clear message
git commit -m "Bump version to 1.0.4"

# Push to GitHub
git push origin main
```

**Verify:**
```bash
# Check that commit was pushed
git log -1 --oneline
```

### Step 5: Wait for CI/CD Workflows

Before creating the release, ensure all automated checks pass:

1. **Go to GitHub Actions page:**
   ```
   https://github.com/YOUR_USERNAME/BM6/actions
   ```

2. **Wait for workflows to complete:**
   - CodeQL Advanced ✓
   - HACS Validation ✓
   - Hassfest Validation ✓

3. **All checks must be green** before proceeding

**Using GitHub CLI:**
```bash
# Wait for workflows to complete
gh run watch

# Check status of latest run
gh run list --limit 1
```

**If any checks fail:**
- Review the error logs
- Fix the issues
- Commit and push fixes
- Wait for checks to pass again

### Step 6: Create Git Tag (Optional but Recommended)

While the GitHub release will create a tag automatically, you can create it locally first:

```bash
# Create annotated tag with version number
git tag -a v1.0.4 -m "Release version 1.0.4"

# Push tag to GitHub
git push origin v1.0.4

# Verify tag was created
git tag -l
```

**Tag Format:**
- Must start with `v` (lowercase)
- Followed by version number
- Example: `v1.0.4`, `v1.1.0`, `v2.0.0`

### Step 7: Create GitHub Release

#### Option A: Using GitHub Web UI

1. **Navigate to Releases:**
   ```
   https://github.com/YOUR_USERNAME/BM6/releases
   ```

2. **Click "Draft a new release"**

3. **Choose or create tag:**
   - Click "Choose a tag"
   - Type: `v1.0.4` (must match version with `v` prefix)
   - Click "Create new tag: v1.0.4 on publish"

4. **Target branch:**
   - Ensure target is `main`

5. **Release title:**
   - Format: `v1.0.4` or `Version 1.0.4` or `BM6 v1.0.4`
   - Examples:
     - `v1.0.4`
     - `Version 1.0.4 - Bug Fixes`
     - `BM6 v1.1.0 - New Features`

6. **Release description:**

   Copy from CHANGELOG.md and expand with details:

   ```markdown
   ## What's Changed
   - Fixed bug in battery percentage calculation that caused incorrect readings near max voltage
   - Improved Bluetooth connection stability during network interruptions
   - Updated Polish translations for new configuration options

   ## Installation

   ### HACS (Recommended)
   1. Open HACS in Home Assistant
   2. Go to Integrations
   3. Search for "BM6"
   4. Click Install
   5. Restart Home Assistant

   ### Manual Installation
   1. Download `bm6.zip` from the assets below
   2. Extract to `custom_components/bm6/` in your Home Assistant config directory
   3. Restart Home Assistant

   ## Upgrade Notes
   - No breaking changes in this release
   - Existing configurations will continue to work
   - Simply update and restart

   ## Requirements
   - Home Assistant 2025.1.1 or newer
   - Bluetooth adapter or ESPHome Bluetooth proxy

   ## Full Changelog
   **Full Changelog**: https://github.com/YOUR_USERNAME/BM6/compare/v1.0.3...v1.0.4
   ```

7. **Set as latest release:**
   - ✓ Check "Set as the latest release"
   - ⚠️ Only uncheck this for pre-releases or hotfixes

8. **Pre-release (optional):**
   - For beta versions, check "Set as a pre-release"
   - Example: `v1.1.0-beta.1`

9. **Click "Publish release"**

#### Option B: Using GitHub CLI

```bash
# Create release with auto-generated notes
gh release create v1.0.4 \
  --title "Version 1.0.4" \
  --notes "$(cat <<'EOF'
## What's Changed
- Fixed bug in battery percentage calculation
- Improved Bluetooth connection stability
- Updated Polish translations

## Installation
Download bm6.zip from the assets below and extract to custom_components/bm6/

## Full Changelog
https://github.com/YOUR_USERNAME/BM6/compare/v1.0.3...v1.0.4
EOF
)"

# Or use auto-generated notes from commits
gh release create v1.0.4 \
  --title "Version 1.0.4" \
  --generate-notes
```

**For pre-releases:**
```bash
gh release create v1.1.0-beta.1 \
  --title "Version 1.1.0 Beta 1" \
  --prerelease \
  --notes "Beta release for testing new features"
```

### Step 8: Monitor Release Workflow

Once you publish the release, the automated release workflow triggers:

1. **Watch the workflow run:**
   ```
   https://github.com/YOUR_USERNAME/BM6/actions/workflows/release.yml
   ```

2. **Monitor progress:**
   ```bash
   # Using GitHub CLI
   gh run watch

   # Or check status
   gh run list --workflow=release.yml --limit 1
   ```

3. **Workflow should complete in 2-5 minutes**

**Expected workflow steps:**
1. ✓ Checkout repository
2. ✓ Adjust version numbers (updates const.py and manifest.json)
3. ✓ Zip the integration directory
4. ✓ Sign release package with Sigstore
5. ✓ Upload ZIP file to release

### Step 9: Verify Release Assets

Once the workflow completes:

1. **Go back to the release page:**
   ```
   https://github.com/YOUR_USERNAME/BM6/releases/tag/v1.0.4
   ```

2. **Verify assets are present:**
   - ✓ `bm6.zip` - Integration package
   - ✓ `bm6.zip.sigstore` - Cryptographic signature (optional)

3. **Download and verify the ZIP:**
   ```bash
   # Download the release asset
   gh release download v1.0.4

   # Verify ZIP contents
   unzip -l bm6.zip

   # Should show:
   # - __init__.py
   # - manifest.json
   # - const.py
   # - config_flow.py
   # - coordinator.py
   # - sensor.py
   # - translations/
   # - etc.
   ```

4. **Verify version numbers in ZIP:**
   ```bash
   # Extract and check version
   unzip -q bm6.zip -d /tmp/bm6-test
   grep "VERSION = " /tmp/bm6-test/const.py
   grep '"version"' /tmp/bm6-test/manifest.json

   # Should both show: 1.0.4
   ```

### Step 10: Test Installation

Before announcing the release, test the installation:

#### Test with HACS (if applicable)

1. Add repository to HACS as custom repository
2. Install from HACS
3. Restart Home Assistant
4. Verify integration loads correctly
5. Test basic functionality

#### Test Manual Installation

```bash
# Download release
wget https://github.com/YOUR_USERNAME/BM6/releases/download/v1.0.4/bm6.zip

# Extract to test Home Assistant instance
unzip bm6.zip -d /path/to/homeassistant/custom_components/bm6/

# Restart Home Assistant
# Verify integration works
```

#### Verification Checklist

- [ ] Integration appears in integrations list
- [ ] Can add new device through UI
- [ ] All sensors populate with data
- [ ] No errors in logs
- [ ] Version shows correctly in integration info

---

## What the Automation Does

When you publish a GitHub release, the `.github/workflows/release.yml` workflow automatically:

### 1. Checks Out Code
```yaml
- name: "Checkout the repository"
  uses: "actions/checkout@v4.2.1"
```
Retrieves the code at the release tag.

### 2. Adjusts Version Numbers
```bash
version="${{ github.event.release.tag_name }}"
version="${version,,}"        # Convert to lowercase
version="${version#v}"        # Remove 'v' prefix

# Updates custom_components/bm6/const.py
sed -i "/^VERSION.*=./c\VERSION = \"${version}\"" "$BM6_ROOT_DIR/const.py"

# Updates custom_components/bm6/manifest.json
jq ".version = \"${version}\"" "$BM6_ROOT_DIR/manifest.json" > "$BM6_ROOT_DIR/manifest.json.tmp"
mv "$BM6_ROOT_DIR/manifest.json.tmp" "$BM6_ROOT_DIR/manifest.json"
```

**Note:** This means even if you forget to update version numbers manually, the workflow will set them based on the release tag. However, it's still best practice to update them before creating the release.

### 3. Creates ZIP Package
```bash
cd custom_components/bm6
zip bm6.zip -r ./
```
Packages the entire integration directory.

### 4. Signs the Package
```yaml
- name: "Sign release package"
  uses: sigstore/gh-action-sigstore-python@v3.0.0
  with:
    inputs: "${{ env.BM6_ROOT_DIR }}/bm6.zip"
```

**Sigstore Signing:**
- Creates cryptographic signature for package verification
- Uses keyless signing (no key management required)
- Provides transparency log entry
- Users can verify package authenticity

**Verification:**
```bash
# Users can verify the signature
pip install sigstore
sigstore verify --bundle bm6.zip.sigstore bm6.zip
```

### 5. Uploads to Release
```yaml
- name: "Upload the ZIP file to the release"
  uses: softprops/action-gh-release@v2.2.1
  with:
    files: ${{ env.BM6_ROOT_DIR }}/bm6.zip
```
Attaches `bm6.zip` to the GitHub release assets.

### Workflow Permissions

The workflow requires specific permissions:
```yaml
permissions:
  contents: write      # Upload assets to release
  id-token: write      # Sign with Sigstore
```

These are automatically granted when the workflow runs on release events.

---

## Post-Release Tasks

After the release is published and verified:

### 1. Announce the Release

#### GitHub Discussions
If enabled, post announcement:
```markdown
# BM6 v1.0.4 Released

We're happy to announce the release of BM6 v1.0.4!

## What's New
- Fixed bug in battery percentage calculation
- Improved Bluetooth connection stability
- Updated Polish translations

## Upgrade Instructions
[Instructions here]

## Download
https://github.com/YOUR_USERNAME/BM6/releases/tag/v1.0.4
```

#### Home Assistant Community Forum
Post in the appropriate integration thread or create new one.

#### Social Media
If applicable, announce on Twitter, Mastodon, etc.

### 2. Update Documentation Sites

If you have external documentation:
- Update version numbers
- Update screenshots if UI changed
- Update feature lists
- Update compatibility matrix

### 3. Monitor for Issues

After release, actively monitor:

#### GitHub Issues
```bash
# Watch for new issues
gh issue list --label "bug" --limit 10
```

#### Home Assistant Logs
If you have telemetry or users report issues, look for patterns.

#### Community Feedback
- Home Assistant forums
- Discord channels
- Reddit posts

### 4. Update Project Board (Optional)

If using GitHub Projects:
- Move completed issues to "Done"
- Close milestone for this version
- Create milestone for next version

### 5. Notify HACS (if listed)

If your integration is in the HACS default repository:
- HACS automatically detects new releases
- New version appears in HACS within 24 hours
- No manual notification needed

If you're a custom repository:
- Users with your repo added will see the update automatically

### 6. Tag Release in Dependabot (if using)

Dependabot will automatically update if you use it in other projects.

---

## Troubleshooting

### Release Workflow Fails

#### Problem: "Version number mismatch"

**Cause:** const.py and manifest.json have different versions before release.

**Solution:**
```bash
# Check current versions
grep "VERSION = " custom_components/bm6/const.py
grep '"version"' custom_components/bm6/manifest.json

# They must match! If not:
# 1. Fix the discrepancy
# 2. Commit and push
# 3. Delete the failed release
# 4. Delete the tag:
git tag -d v1.0.4
git push origin :refs/tags/v1.0.4

# 5. Create release again
```

#### Problem: "Permission denied" when uploading assets

**Cause:** Workflow doesn't have write permissions.

**Solution:**
1. Go to: Settings > Actions > General > Workflow permissions
2. Select "Read and write permissions"
3. Click "Save"
4. Re-run the workflow

#### Problem: Sigstore signing fails

**Cause:** OIDC token issues or Sigstore service down.

**Solution:**
```bash
# Check Sigstore status
curl https://status.sigstore.dev/

# If down, wait and re-run workflow
# If persistent, signing can be made optional
```

#### Problem: ZIP file is missing files

**Cause:** Incorrect zip command or directory structure.

**Solution:**
Verify directory structure:
```bash
custom_components/bm6/
├── __init__.py
├── manifest.json
├── const.py
└── ...
```

Check workflow logs for ZIP contents.

### Release Not Appearing in HACS

#### Problem: HACS doesn't show new version

**Cause:** HACS cache hasn't updated yet.

**Solution:**
1. Wait 24 hours for automatic update
2. Or force update in HACS:
   - HACS > 3 dots menu > Custom repositories
   - Find your integration
   - Click "Redownload"

#### Problem: "Invalid version" in HACS

**Cause:** Tag format doesn't match HACS requirements.

**Solution:**
- Tag must start with `v`
- Must be semantic versioning
- Examples: `v1.0.4`, `v1.1.0`, `v2.0.0`
- Not: `1.0.4`, `version-1.0.4`, `release-1.0.4`

### Users Report Issues After Update

#### Problem: Sensors stopped working after update

**Quick Response:**
1. Ask for Home Assistant logs
2. Check compatibility with their HA version
3. Look for common patterns in reports

**Resolution:**
1. Identify the issue
2. Create hotfix (see next section)
3. Release patched version quickly

#### Problem: Configuration breaks after update

**Breaking Change Protocol:**
1. Acknowledge the issue immediately
2. Provide migration guide
3. Consider backward compatibility fix
4. Document in CHANGELOG as breaking change

---

## Hotfix Releases

For critical bugs that need immediate fixes:

### When to Hotfix

Release hotfix for:
- Security vulnerabilities
- Data loss bugs
- Integration completely broken
- Critical feature not working

**Don't hotfix for:**
- Minor UI issues
- Non-critical bugs
- Feature requests
- Documentation typos

### Hotfix Process

```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/1.0.5

# 2. Make the fix
# Edit files...

# 3. Test thoroughly
pytest tests/
# Test in real Home Assistant

# 4. Update version (PATCH bump)
# Update const.py: VERSION = "1.0.5"
# Update manifest.json: "version": "1.0.5"

# 5. Update CHANGELOG
# Add:
## 1.0.5 (Hotfix)
- Fixed critical bug causing sensor failures

# 6. Commit
git add .
git commit -m "Hotfix: Fix critical sensor failure"

# 7. Merge to main
git checkout main
git merge hotfix/1.0.5
git push origin main

# 8. Create release immediately
gh release create v1.0.5 \
  --title "v1.0.5 (Hotfix)" \
  --notes "Critical hotfix for sensor failures in v1.0.4"

# 9. Announce urgently
# Notify users to update immediately
```

### Hotfix Communication

```markdown
# 🚨 Critical Hotfix: v1.0.5 Released

A critical bug was discovered in v1.0.4 that causes sensor failures.

## Impact
- Affects: All users on v1.0.4
- Severity: High
- Sensors may stop reporting data

## Action Required
Please update to v1.0.5 immediately.

## Fixed
- Critical sensor failure bug

## How to Update
[Update instructions]
```

---

## Rolling Back a Release

If a release has critical issues and hotfix isn't immediate:

### Mark Release as Non-Latest

```bash
# Via GitHub CLI
gh release edit v1.0.4 --latest=false

# Via Web UI:
# 1. Go to release page
# 2. Click "Edit"
# 3. Uncheck "Set as the latest release"
# 4. Save
```

### Create Warning Notice

Add warning to release description:
```markdown
# ⚠️ WARNING: Do Not Use This Release

This release has been superseded by v1.0.5 due to critical bugs.

Please use v1.0.5 instead: https://github.com/YOUR_USERNAME/BM6/releases/tag/v1.0.5

## Known Issues
- Sensors fail to report data
- Bluetooth connection unstable

This release is kept for historical purposes only.
```

### Don't Delete Releases

**Never delete a published release** because:
- Users may have already downloaded it
- Breaks version history
- Confuses HACS
- Breaks changelog links

Instead, mark as non-latest and publish fixed version.

---

## Release Checklist Template

Copy this checklist for each release:

```markdown
# Release v1.0.X Checklist

## Pre-Release
- [ ] All tests pass
- [ ] Linters pass
- [ ] HACS validation passes
- [ ] Hassfest validation passes
- [ ] CodeQL scan passes
- [ ] Manual testing complete
- [ ] Documentation updated

## Version Update
- [ ] Updated const.py to v1.0.X
- [ ] Updated manifest.json to v1.0.X
- [ ] Updated CHANGELOG.md
- [ ] Versions match in both files
- [ ] Committed and pushed changes

## Release Creation
- [ ] All CI/CD checks green on main
- [ ] Created tag v1.0.X
- [ ] Created GitHub release
- [ ] Release workflow completed successfully
- [ ] bm6.zip present in release assets

## Verification
- [ ] Downloaded and inspected ZIP
- [ ] Version numbers correct in ZIP
- [ ] Test installation successful
- [ ] Integration loads in HA
- [ ] All sensors working

## Post-Release
- [ ] Announced release
- [ ] Monitoring issues
- [ ] HACS updated (wait 24h)

## Notes
[Any special notes about this release]
```

---

## Additional Resources

### Documentation Links
- [Semantic Versioning](https://semver.org/)
- [GitHub Releases Guide](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [Sigstore Documentation](https://www.sigstore.dev/)
- [HACS Documentation](https://hacs.xyz/)

### Internal Documentation
- [GitHub Workflows](workflows.md) - Details on release.yml workflow
- [Configuration Directory](config.md) - Testing environment setup
- [VS Code Configuration](vscode.md) - Development environment

### Home Assistant Resources
- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [Integration Manifest](https://developers.home-assistant.io/docs/creating_integration_manifest)
- [Integration Quality Scale](https://developers.home-assistant.io/docs/integration_quality_scale_index)

---

## Questions or Issues?

If you encounter problems not covered in this guide:

1. **Check workflow logs:**
   ```bash
   gh run view --log
   ```

2. **Review previous successful releases:**
   ```bash
   gh release list
   ```

3. **Ask for help:**
   - GitHub Discussions
   - Home Assistant Developer Community
   - Stack Overflow

4. **Update this documentation:**
   - If you solve a new problem, add it to this guide
   - Help future maintainers avoid the same issues
