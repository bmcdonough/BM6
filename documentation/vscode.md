# VS Code Workspace Configuration

This document describes the Visual Studio Code workspace configuration for the BM6 project, located in `.vscode/`.

## Overview

The workspace includes three configuration files that provide spell checking, linting, and editor settings optimized for Home Assistant integration development.

---

## Files

### `settings.json`

**File:** `.vscode/settings.json`

Workspace settings that configure the Python development environment.

#### Python Linting Configuration

**Pylint (Primary Linter)**
- **Enabled:** Yes
- **Django Support:** Loads `pylint_django` plugin for Django/Home Assistant compatibility
- **Disabled Rules:**
  - `C0111` - Missing docstring warnings disabled

**Ruff (Modern Fast Linter)**
- **Enabled:** Yes
- **Selected Rules:**
  - `E` - PEP 8 error codes
  - `W` - PEP 8 warning codes
  - `F` - PyFlakes error codes
  - `D` - PEP 257 docstring conventions
  - `I` - Import sorting
- **Max Line Length:** 88 characters (Black formatter standard)

**Disabled Linters**
- Flake8 - Disabled (using Ruff instead)
- mypy - Disabled (type checking not enforced)

**Linting Behavior**
- **Lint on Save:** Enabled - Files are automatically linted when saved

#### File Associations
- `*.yaml` files are associated with `home-assistant` language mode for proper syntax highlighting and IntelliSense

#### Benefits
- Catches common Python errors before commit
- Enforces code style consistency
- Django plugin prevents false positives with Home Assistant patterns
- Ruff provides fast, comprehensive linting
- Home Assistant YAML support improves configuration editing

---

### `cspell.json`

**File:** `.vscode/cspell.json`

Configuration for the Code Spell Checker extension (Street Side Software.code-spell-checker).

#### Basic Configuration
- **Version:** 0.2
- **Default Language:** English (en)
- **Primary Dictionary:** Python words from `python-words.txt`

#### Custom Dictionaries

**Python Dictionary**
- **Location:** `./python-words.txt`
- **Auto-add:** Enabled - New words can be added to dictionary
- **Purpose:** Python-specific terms and function names

**Language-Specific Overrides**

1. **Polish Dictionary**
   - **Files:** `**/pl.json`
   - **Language:** Polish (pl)
   - **Dictionary:** `cspell-dict-pl-pl`
   - **Purpose:** Validates Polish translation files

2. **English Dictionary**
   - **Files:** `**/en.json`
   - **Language:** English (en)
   - **Dictionary:** `cspell-dict-en-us`
   - **Purpose:** Validates English translation files

#### Ignored Paths
The following directories/files are excluded from spell checking:
- `**/node_modules/**` - npm dependencies
- `**/dist/**` - Build output
- `**/venv/**` - Python virtual environment
- `requirements.txt` - Package names not relevant for spell check

#### Ignored Patterns (Regex)
- `/#.*#/` - Comments
- `/\".*\"/` - Double-quoted strings
- `/'.*'/` - Single-quoted strings
- `/\`.*\`/` - Template literals

These patterns prevent false positives in code strings and comments.

#### Custom Words List
Project-specific technical terms recognized by the spell checker:

**People & Brand Names**
- Rafał Drzymała - Developer name
- Sealey - Brand name
- QUICKLYNKS - Product/brand name

**Python/Technical Terms**
- asyncio - Async I/O library
- aiofiles - Async file operations
- bytearray - Python data type
- dataclass, dataclasses - Python decorators
- staticmethod - Python decorator
- isinstance - Python built-in
- repr - Python built-in

**Package Names**
- awesomeversion - Version comparison library
- NumPy - Numerical computing library
- pandas - Data analysis library
- PyPI - Python Package Index
- googletrans - Translation library

**Home Assistant Terms**
- hacs - Home Assistant Community Store
- hass - Home Assistant abbreviation
- homeassistant - Full project name

**Battery/Technical Acronyms**
- MILLIWATT - Power measurement unit
- RSSI - Received Signal Strength Indicator
- VRLA - Valve Regulated Lead Acid battery

**UI/UX Terms**
- Acce - Likely abbreviation for "Accept"
- ANCEL - Likely abbreviation for "Cancel"
- Dece - Likely abbreviation for "Decline"

#### Benefits
- Catches typos in code comments and documentation
- Supports multilingual projects (Polish + English)
- Reduces false positives with technical term dictionary
- Improves code documentation quality

---

### `python-words.txt`

**File:** `.vscode/python-words.txt`

Custom dictionary of Python-specific terms for spell checking.

#### Words List
1. **getmtime** - `os.path.getmtime()` function for file modification time
2. **googletrans** - Python translation library package name
3. **isinstance** - Python built-in function for type checking
4. **repr** - Python built-in function for object representation

#### Purpose
- Supplements main cspell.json word list
- Stores common Python function names
- Prevents spell checker from flagging valid Python syntax
- Can be extended with additional Python-specific terms

#### Usage
Words are automatically added when using the Code Spell Checker's "Add to Dictionary" feature if `addWords: true` is configured in `cspell.json`.

---

## Setup Instructions

### Required VS Code Extensions

1. **Python** (ms-python.python)
   - Python language support
   - Integrated linting and debugging
   - Required for settings.json linting configuration

2. **Pylint** (ms-python.pylint)
   - Python linting support
   - Required for pylint configuration

3. **Ruff** (charliermarsh.ruff)
   - Fast Python linter
   - Required for ruff configuration

4. **Code Spell Checker** (streetsidesoftware.code-spell-checker)
   - Spell checking for code and comments
   - Required for cspell.json configuration

5. **Home Assistant Config Helper** (optional)
   - Provides syntax highlighting for Home Assistant YAML files
   - Supports the `*.yaml: home-assistant` file association

### Installation

Install extensions via VS Code:
```
ext install ms-python.python
ext install ms-python.pylint
ext install charliermarsh.ruff
ext install streetsidesoftware.code-spell-checker
```

Or through the Extensions marketplace (Ctrl+Shift+X).

### Python Dependencies

Install required linting tools:
```bash
pip install pylint pylint-django ruff
```

These should be included in your development requirements.

---

## Recommended Workflow

### 1. Opening the Project
When you open the project in VS Code:
- The workspace settings automatically load
- Linters activate for Python files
- Spell checker begins monitoring files

### 2. Writing Code
As you code:
- Spelling errors appear with blue squiggles
- Linting errors/warnings appear with red/yellow squiggles
- Hovering shows detailed error messages

### 3. Saving Files
When you save:
- Automatic linting runs (lint on save enabled)
- Errors appear in Problems panel (Ctrl+Shift+M)

### 4. Fixing Issues

**Spelling Errors:**
- Right-click on underlined word
- Choose "Add to Dictionary" to add to python-words.txt
- Or select correct spelling from suggestions

**Linting Errors:**
- Click on error in Problems panel to navigate to code
- Follow suggested fix or disable specific rule if needed
- Use Quick Fix (Ctrl+.) for automated corrections

### 5. Configuration Files
When editing YAML:
- Files automatically use home-assistant syntax
- IntelliSense provides Home Assistant-specific completions

---

## Customization

### Adding New Words to Dictionary

**Method 1: Through UI**
1. Right-click on spell-check-flagged word
2. Select "Add to Dictionary"
3. Choose "python-words.txt"

**Method 2: Manual Edit**
1. Open `.vscode/cspell.json`
2. Add word to `words` array
3. Save file

### Disabling Linting Rules

**Pylint:**
Add to `python.linting.pylintArgs` in settings.json:
```json
"--disable=C0111,W0212"
```

**Ruff:**
Modify `python.linting.ruffArgs`:
```json
"--ignore=E501,D100"
```

### Changing Line Length
Update both linters if changing from 88:
```json
"python.linting.ruffArgs": [
    "--max-line-length=120"
]
```

### Ignoring Additional Paths
Add to `cspell.json` ignorePaths:
```json
"ignorePaths": [
    "**/node_modules/**",
    "**/dist/**",
    "**/venv/**",
    "requirements.txt",
    "**/build/**"
]
```

---

## Troubleshooting

### Linters Not Working

**Check Extension Installation:**
```
code --list-extensions | grep python
```

**Verify Python Interpreter:**
- Open Command Palette (Ctrl+Shift+P)
- Run "Python: Select Interpreter"
- Choose project's virtual environment

**Check Output Panel:**
- View > Output
- Select "Python" or "Pylint" from dropdown
- Review error messages

### Spell Checker Not Working

**Verify Extension:**
```
code --list-extensions | grep code-spell-checker
```

**Check Language:**
- Right-click in file
- Select "Spell Checker" > "Show Current Language"
- Should show "en" for English files

**Reload Configuration:**
- Open Command Palette
- Run "Developer: Reload Window"

### False Positives

**Spell Checker:**
- Add words to dictionary as described above
- Or use `// cspell:disable-next-line` comment

**Linting:**
- Add `# pylint: disable=rule-name` comment
- Or `# noqa: rule-code` for Ruff

---

## Best Practices

1. **Commit Configuration** - The .vscode folder should be committed to ensure all team members have consistent settings

2. **Document Custom Words** - Add comments when adding unusual technical terms to dictionaries

3. **Regular Updates** - Keep linting rules up-to-date with Home Assistant coding standards

4. **Extension Versions** - Document required extension versions if compatibility issues arise

5. **Team Consistency** - All team members should use the same extensions and configuration

6. **Language-Specific** - Maintain separate dictionaries for different languages (already configured)

7. **Avoid Disabling** - Don't disable linting rules globally; use inline comments for specific cases

---

## Related Links

- [VS Code Python Documentation](https://code.visualstudio.com/docs/python/python-tutorial)
- [Pylint Documentation](https://pylint.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Code Spell Checker Extension](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)
- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
