# Pylero Agent Rules

## Project Overview

Pylero is a Python SDK wrapping the Polarion WSDL/SOAP API. It provides native Python access to Polarion objects (work items, test runs, documents, plans, etc.) via dynamically generated properties from WSDL definitions.

## Repository Structure

```
src/pylero/          # Main package (60+ modules)
  base_polarion.py   # Base class for all Polarion objects (core)
  session.py         # Session management
  server.py          # Server connection
  cli/cmd.py         # Click-based CLI interface
  pylero.cfg         # Default config template
src/unit_tests/      # Unit test suite
scripts/             # Entry points (pylero, pylero-cmd)
doc/, docs/          # Documentation
.tito/               # RPM release management (Fedora Copr)
```

## Python Environment

- **Supported versions**: Python 3.10, 3.11, 3.12, 3.13
- **Package manager**: Use `uv` for virtual environments and package installation
- **Dependencies**: `suds` (SOAP client), `click` (CLI)
- **Dev dependencies**: `pre-commit`, `ruff`

```bash
uv venv
uv pip install -e .
uv pip install pre-commit ruff
```

## Code Quality

### Pre-commit (mandatory)

Pre-commit hooks must be installed and must pass before committing:

```bash
pre-commit install
pre-commit run --files <changed-files>
```

Configured hooks:
- `trailing-whitespace`
- `end-of-file-fixer`
- `debug-statements`
- `detect-private-key`
- `ruff --fix` (linting with auto-fix)
- `ruff-format` (formatting)

### Ruff Configuration

Defined in `pyproject.toml`:
- **Line length**: 120 characters
- **Target version**: Python 3.13
- **Lint rules**: E (pycodestyle), F (Pyflakes), I (isort)
- **Ignored**: E501 (line too long)
- **Quote style**: double quotes
- **Import sorting**: isort with `pylero` as known first-party

### Code Style

- 4-space indentation (Python standard)
- PEP8 snake_case for functions/variables, CamelCase for classes
- Double quotes for strings
- Max line length 120 (soft, E501 ignored)

## Testing

- **Framework**: nose2 with coverage plugin
- **Test runner**: `python tier_tests.py {tier}`
  - `tier0` - Basic attribute tests
  - `tier1` - Integration tests (requires Polarion connection)
  - `all` - Complete suite
- **Tox**: Used for release scaffolding, not for regular testing
- **Unit tests location**: `src/unit_tests/`
- **Note**: All tests require a live Polarion instance connection. The upstream CI only runs pre-commit/linting checks, not the test suite. Do not expect tests to pass without a configured Polarion server.

## Git Workflow

- **Default branch**: `main`
- **PRs**: Rebase from `main`, clear commit messages, brief description
- **CI**: GitHub Actions runs pre-commit checks on PR (Python 3.10-3.13 matrix)
- Always run `pre-commit run -a` before pushing

## CI/CD

- **PR checks**: `.github/workflows/pull_request.yml` - Pre-commit on Python 3.10-3.13
- **PyPI publish**: `.github/workflows/publish-to-pypi.yml` - On release, via OIDC trusted publisher
- **Security**: `.github/workflows/codeql-analysis.yml` - CodeQL analysis

## Architecture Notes

- `BasePolarion` is the parent class for all WSDL objects - changes here affect everything
- Properties are dynamically generated from `_cls_suds_map` dictionaries
- Enum validation happens before server submission via `check_valid_field_values`
- `_cache` is a class-level dict shared across instances for enum/field caching
- The SOAP/WSDL API is in maintenance mode; Polarion is moving to REST API

## Release Management

- **PyPI**: Published via GitHub Actions on release creation
- **RPM**: Tito-based releases for Fedora Copr
- **Versioning**: `setuptools_scm` (git tag-based)
