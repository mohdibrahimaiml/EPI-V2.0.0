# PyPI Upload Guide for EPI Recorder

This guide explains how to build and upload the `epi-recorder` package to PyPI.

## Prerequisites

### 1. Install build tools
```bash
pip install --upgrade build twine
```

### 2. Create PyPI account
- Production PyPI: https://pypi.org/account/register/
- Test PyPI: https://test.pypi.org/account/register/

### 3. Configure PyPI credentials

Create or edit `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...YOUR_TOKEN_HERE...

[testpypi]
username = __token__
password = pypi-AgENdGVzdC5weXBpLm9yZw...YOUR_TOKEN_HERE...
```

**How to get tokens:**
- PyPI: https://pypi.org/manage/account/token/
- Test PyPI: https://test.pypi.org/manage/account/token/

**Windows location:** `C:\Users\YourUsername\.pypirc`

**Permissions:** Ensure file is readable only by you.

---

## Build Process

### 1. Clean previous builds
```bash
# Remove old distributions
rm -r dist/
rm -r build/
rm -r *.egg-info
```

On Windows PowerShell:
```powershell
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue
```

### 2. Build the package
```bash
python -m build
```

This creates:
- `dist/epi_recorder-1.0.0.tar.gz` (source distribution)
- `dist/epi_recorder-1.0.0-py3-none-any.whl` (wheel)

### 3. Check the distribution
```bash
twine check dist/*
```

Expected output:
```
Checking dist/epi_recorder-1.0.0-py3-none-any.whl: PASSED
Checking dist/epi_recorder-1.0.0.tar.gz: PASSED
```

---

## Upload to Test PyPI (Recommended First)

### 1. Upload to Test PyPI
```bash
twine upload --repository testpypi dist/*
```

### 2. Test installation from Test PyPI
```bash
# Create fresh virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ epi-recorder

# Test it works
epi --help
python -c "from epi_recorder import record; print('Success!')"
```

### 3. Verify functionality
```bash
# Run a quick test
python -c "
from epi_recorder import record
with record('test.epi', workflow_name='Test'):
    print('Testing PyPI installation')
"

# Verify the file
epi verify test.epi
```

---

## Upload to Production PyPI

**⚠️ WARNING: You cannot delete or modify files on PyPI once uploaded for a given version!**

### 1. Final checks
- [ ] All tests pass: `pytest tests/ -v`
- [ ] Version number is correct in `pyproject.toml`
- [ ] CHANGELOG.md is updated
- [ ] README.md is accurate
- [ ] LICENSE file exists

### 2. Upload to PyPI
```bash
twine upload dist/*
```

### 3. Verify on PyPI
Visit: https://pypi.org/project/epi-recorder/

### 4. Test installation
```bash
# In a fresh environment
pip install epi-recorder

# Test
epi --help
python -c "from epi_recorder import record; print('Success!')"
```

---

## Version Management

### Bumping versions

Edit `pyproject.toml`:
```toml
[project]
name = "epi-recorder"
version = "1.0.1"  # Increment this
```

**Semantic Versioning:**
- **MAJOR** (1.x.x) - Breaking changes
- **MINOR** (x.1.x) - New features, backwards compatible
- **PATCH** (x.x.1) - Bug fixes, backwards compatible

### Update CHANGELOG.md

Add new section:
```markdown
## [1.0.1] - 2024-11-01

### Fixed
- Bug in artifact handling

### Added
- New feature X
```

### Tag the release
```bash
git tag -a v1.0.1 -m "Release version 1.0.1"
git push origin v1.0.1
```

---

## Troubleshooting

### "File already exists" error
You cannot reupload the same version. You must bump the version number in `pyproject.toml`.

### "Invalid distribution" error
Run `twine check dist/*` to see specific issues.

### README not rendering on PyPI
Ensure `pyproject.toml` has:
```toml
readme = {file = "README.md", content-type = "text/markdown"}
```

### Missing files in package
Check `MANIFEST.in` and ensure all required files are listed.

To verify what's included:
```bash
tar -tzf dist/epi_recorder-1.0.0.tar.gz
```

---

## CI/CD Integration (Future)

### GitHub Actions example

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
      run: twine upload dist/*
```

Store `PYPI_TOKEN` in repository secrets.

---

## Quick Reference

```bash
# Clean → Build → Check → Upload to Test → Upload to Production

# Clean
rm -r dist/ build/ *.egg-info

# Build
python -m build

# Check
twine check dist/*

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

---

## Support

For issues:
- PyPI help: https://pypi.org/help/
- Twine docs: https://twine.readthedocs.io/
- Packaging guide: https://packaging.python.org/
