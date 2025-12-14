# Changelog

All notable changes to the EPI Recorder project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2025-12-14

### Usability (The "Foolproof" Update)
- **New `epi init` command**: A wizard that sets up keys, creates a demo script, and verifies the environment automatically.
- **New `epi doctor` command**: Self-diagnosis tool to check Python environment, keys, browser, and system paths.
- **Auto-Keys**: `epi run` now silently auto-generates keys if they are missing (no more "Unsigned" errors).
- **Empty Script Detection**: `epi run` warns if a script executed but recorded zero steps.
- **Windows Reliability**: Fixed Unicode/Emoji crashes on Windows terminals and path handling issues.
- **Smart UX**: Fixed interactive file picker to verify user inputs and properly list new scripts.
- **Path Fixer**: Included `epi_setup.py` to fix "command not recognized" errors on Windows.

## [2.0.0] - 2025-12-07
- Major release with full CLI and verification system.

## [1.1.0] - 2025-11-23

### Added
- **Human decision metadata** to recordings: goal, notes, metrics, approved_by, tags
- **CLI flags**: --goal, --notes, --metric, --approved-by, --tag
- **Python API**: @record(...) and with record(... ) accept metadata parameters
- **Enhanced listing**: epi ls displays metadata summary
- **Viewer improvements**: Shows metadata header when present

### Technical
- Extended ManifestModel schema with new optional metadata fields
- Updated CLI run command to parse and store metadata
- Enhanced viewer.html to display metadata section
- Improved epi ls output formatting for metadata

## [1.0.0] - 2024-10-30

### Added
- **Python API wrapper** for seamless integration into Python projects
  - Context manager interface with `record()` and `EpiRecorderSession`
  - Automatic OpenAI SDK patching for transparent LLM call recording
  - Manual logging methods: `log_step()`, `log_llm_request()`, `log_llm_response()`, `log_artifact()`
  - Thread-local session management for concurrent workflows
  - Automatic environment capture and packaging
  - Cryptographic signing by default with Ed25519

- **CLI commands** for shell integration
  - `epi record` - Record command execution
  - `epi verify` - Verify .epi file integrity and authenticity
  - `epi view` - Open .epi file in browser viewer
  - `epi keys` - Manage Ed25519 keypairs

- **Core features**
  - Self-contained `.epi` file format (ZIP-based)
  - Automatic secret redaction (15+ patterns)
  - Ed25519 cryptographic signatures
  - SHA-256 content addressing for artifacts
  - Environment snapshot capture
  - Structured JSON manifest with schema validation

- **Static web viewer**
  - Interactive timeline visualization
  - LLM chat bubble display
  - Trust level indicators
  - Artifact previews
  - Zero code execution (pure JSON rendering)

- **Security**
  - Auto-redaction of API keys, tokens, credentials
  - Ed25519 signatures for authenticity
  - Secure key storage in `~/.epi/keys/`
  - Three-level verification (structural, integrity, authenticity)

- **Documentation**
  - Comprehensive README with quick start guide
  - Python API usage examples
  - CLI command reference
  - Security best practices

### Technical
- Python 3.11+ support
- Cross-platform (Windows, macOS, Linux)
- Pydantic v2 for schema validation
- Rich CLI output with colors and tables
- Typer for command-line interface
- cryptography library for Ed25519
- CBOR2 for binary serialization

### Testing
- 17 unit tests for Python API
- 4 integration tests with mocked OpenAI calls
- 5 example scripts demonstrating various use cases
- 100% test pass rate

## [Unreleased]

### Planned
- PyPI package distribution
- Docker deployment examples
- CI/CD integration templates
- Replay functionality for deterministic reproduction
- Additional LLM provider integrations (Anthropic, Cohere, etc.)
- Web-based .epi file explorer
- Diff tool for comparing .epi files

---

[1.1.0]: https://github.com/epi-project/epi-recorder/releases/tag/v1.1.0
[1.0.0]: https://github.com/epi-project/epi-recorder/releases/tag/v1.0.0