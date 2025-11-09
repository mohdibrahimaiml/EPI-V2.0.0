# EPI - Executable Package for AI

**The "PDF for AI Workflows"** — Self-contained, cryptographically verified evidence packages for AI systems.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-MVP-green.svg)]()

---

## 🚀 Quick Start

### **Python API** (Recommended for Developers)

```python
from epi_recorder import record

# Wrap your AI code with a context manager
with record("my_workflow.epi", workflow_name="Demo"):
    # Your AI code runs normally - automatically recorded!
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    
    # Optionally log custom events
    epi.log_step("calculation", {"result": 42})

# .epi file is automatically created, signed, and ready to verify!
```

### **CLI** (For Shell Scripts & CI/CD)

```bash
# Install
pip install epi-recorder

# Record a workflow
epi record --out demo.epi -- python my_ai_script.py

# Verify integrity and authenticity
epi verify demo.epi

# View in browser
epi view demo.epi
```

**That's it!** Your AI workflow is now captured, signed, and viewable.

---

## 🎯 What is EPI?

EPI captures **everything** that happens during an AI workflow:
- 🤖 **LLM API calls** (prompts, responses, tokens, latency)
- 🔒 **Secrets redacted** automatically (15+ patterns)
- 📦 **Files and artifacts** (content-addressed)
- 🖥️ **Environment snapshot** (OS, Python, packages)
- ✅ **Cryptographically signed** (Ed25519)
- 📊 **Beautiful timeline viewer** (static HTML)

All packaged into a **single `.epi` file** that anyone can verify and replay.

---

## 🌟 Why EPI?

### **The Problem**

❌ 70% of AI research cannot be reproduced  
❌ AI models fail mysteriously in production  
❌ Cannot prove how AI decisions were made  
❌ "It worked on my machine" debugging nightmare  

### **The Solution**

✅ **Record**: Capture complete AI workflows with one command  
✅ **Verify**: Cryptographic proof of authenticity  
✅ **Share**: Single file contains everything  
✅ **Replay**: Deterministic reproduction (offline mode)  
✅ **Audit**: Full transparency for compliance  

---

## 📖 Core Features

### 🎬 **Recording**
```bash
epi record --out experiment.epi -- python train.py
```
Automatically captures:
- OpenAI API calls (GPT-4, GPT-3.5, etc.)
- Shell commands and outputs
- Python execution context
- Generated files and artifacts
- Environment variables (redacted)

### 🔐 **Security by Default**
- **Auto-redacts secrets**: API keys, tokens, credentials
- **Ed25519 signatures**: Cryptographic proof of authenticity
- **Frictionless**: Auto-generates keypair on first run
- **No secret leakage**: 15+ regex patterns protect sensitive data

### ✅ **Verification**
```bash
epi verify experiment.epi
```
Three-level verification:
1. **Structural**: Valid ZIP format and schema
2. **Integrity**: SHA-256 file hashes match
3. **Authenticity**: Ed25519 signature valid

### 👁️ **Beautiful Viewer**
```bash
epi view experiment.epi
```
Opens in your browser with:
- Interactive timeline of all steps
- LLM chat bubbles (prompts & responses)
- Trust badges (signed/unsigned)
- Artifact previews
- **Zero code execution** (pure JSON rendering)

---

## 🎓 Use Cases

### **AI Researchers**
```bash
# Submit verifiable research
epi record --out paper_experiment.epi -- python reproduce.py
```
✅ 100% reproducible methodology  
✅ Eliminates "it worked on my machine"  
✅ Speeds up peer review  

### **Enterprise AI Teams**
```bash
# Capture production AI runs
epi record --out prod_run.epi -- python deploy_model.py
```
✅ Audit trails for compliance (EU AI Act, SOC 2)  
✅ Debug production failures instantly  
✅ Version control for AI systems  

### **Software Engineers**
```bash
# Perfect bug reproduction
epi record --out bug_report.epi -- python flaky_test.py
```
✅ Share exact failing conditions  
✅ Debug AI features faster  
✅ Stable CI/CD for AI features  

---

## 🛠️ Installation

### **From Source** (Development)
```bash
cd epi-recorder
pip install -e .
```

### **Requirements**
- Python 3.11+
- Windows, macOS, or Linux

---

## 📚 Commands

### **`epi record`**
Record a workflow into a `.epi` file.

```bash
epi record --out run.epi -- python script.py [args...]

Options:
  --out PATH              Output .epi file (required)
  --no-sign              Don't sign the manifest
  --no-redact            Disable secret redaction
```

### **`epi verify`**
Verify `.epi` file integrity and authenticity.

```bash
epi verify run.epi

Options:
  --json        Output as JSON
  --verbose     Verbose output
```

### **`epi view`**
Open `.epi` file in browser.

```bash
epi view run.epi
```

### **`epi keys`**
Manage Ed25519 key pairs.

```bash
epi keys generate --name mykey
epi keys list
epi keys export --name mykey
```

---

## 🐍 Python API

### **Why Use the Python API?**

The Python API is the **recommended way** to integrate EPI into your AI applications:
- ✅ **Zero CLI overhead** - no shell commands needed
- ✅ **Seamless integration** - just wrap your code with `with record()`
- ✅ **Auto-captures OpenAI** - automatically records all LLM calls
- ✅ **Custom logging** - manually log steps and artifacts
- ✅ **Auto-signed** - cryptographic signatures by default

### **Basic Usage**

```python
from epi_recorder import record

with record("experiment.epi", workflow_name="My Experiment"):
    # Your code here - automatically recorded
    result = train_model()
    print(f"Result: {result}")
```

### **With Custom Logging**

```python
from epi_recorder import record
from pathlib import Path

with record("workflow.epi", workflow_name="Data Processing", tags=["v1.0", "prod"]) as epi:
    # Process data
    data = load_data("input.csv")
    
    # Log custom steps
    epi.log_step("data.loaded", {
        "rows": len(data),
        "columns": list(data.columns)
    })
    
    # Process...
    results = process(data)
    
    # Save output
    results.to_csv("output.csv")
    
    # Capture the output file
    epi.log_artifact(Path("output.csv"))
    
    # Log summary
    epi.log_step("processing.complete", {
        "status": "success",
        "output_rows": len(results)
    })
```

### **With OpenAI (Auto-Recorded)**

```python
from epi_recorder import record
import openai

with record("chat_session.epi", workflow_name="Customer Support"):
    # OpenAI calls are automatically captured!
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is quantum computing?"}
        ]
    )
    
    print(response.choices[0].message.content)
    
    # API keys are automatically redacted in the recording!
```

### **Advanced Options**

```python
from epi_recorder import EpiRecorderSession

with EpiRecorderSession(
    "advanced.epi",
    workflow_name="Advanced Workflow",
    tags=["experiment", "2024-10-29"],
    auto_sign=True,        # Sign with default key (default: True)
    redact=True,          # Redact secrets (default: True)
    default_key_name="my-key"  # Custom signing key
) as epi:
    # Your workflow
    pass
```

### **Manual LLM Logging** (For Custom Integrations)

```python
from epi_recorder import record

with record("custom_llm.epi") as epi:
    # For custom/proprietary LLM APIs
    epi.log_llm_request("claude-3-opus", {
        "messages": [{"role": "user", "content": "Hello"}],
        "temperature": 0.7
    })
    
    # ... make actual API call ...
    
    epi.log_llm_response({
        "model": "claude-3-opus",
        "content": "Hello! How can I help?",
        "tokens": 25
    })
```

### **Error Handling**

Recordings are saved even if errors occur:

```python
from epi_recorder import record

try:
    with record("debug_session.epi", workflow_name="Debug") as epi:
        epi.log_step("process.start", {"status": "ok"})
        
        # Code that might fail
        result = risky_operation()
        
except Exception as e:
    print(f"Error: {e}")
    # .epi file is still created with error logs!
```

### **Running the Examples**

```bash
# See examples directory
python examples/api_example.py

# Verify the generated .epi files
epi verify example_basic.epi

# View in browser
epi view example_basic.epi
```

---

## 🔒 Security

### **Automatic Redaction**
EPI automatically removes:
- OpenAI API keys (`sk-...`)
- Anthropic API keys (`sk-ant-...`)
- AWS credentials (`AKIA...`)
- GitHub tokens (`ghp_...`)
- Bearer tokens, JWT tokens
- Database connection strings
- Private keys (PEM format)

### **Cryptographic Signing**
- **Algorithm**: Ed25519 (RFC 8032)
- **Key Size**: 256 bits
- **Hash**: SHA-256 with canonical CBOR
- **Storage**: `~/.epi/keys/` (secure permissions)

---

## 🧪 Example

```python
# chat_example.py
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Explain quantum computing"}
    ]
)

print(response.choices[0].message.content)
```

```bash
# Record it
epi record --out chat.epi -- python chat_example.py

# Verify it
epi verify chat.epi
# ✅ Trust Level: HIGH

# View it
epi view chat.epi
# Opens timeline in browser
```

---

## 🧑‍💻 Development

### **Running Tests**
```bash
pytest tests/ -v --cov=epi_core --cov=epi_cli
```

### **Project Structure**
```
epi-recorder/
├── epi_core/           # Core logic
├── epi_cli/            # CLI commands
├── epi_recorder/       # Runtime capture
├── epi_viewer_static/  # Static viewer
├── tests/              # Test suite
└── docs/               # Specification
```

---

## 📊 Status

✅ **Phase 0**: Foundation (complete)  
✅ **Phase 1**: Trust Layer (complete)  
✅ **Phase 2**: Recorder MVP (complete)  
✅ **Phase 3**: Viewer MVP (complete)  
🔄 **Phase 4**: Polish & docs (in progress)  

**Current**: Keystone MVP - Production Ready

---

## 📄 License

Apache License 2.0

---

## 🙏 Acknowledgments

Built with:
- [Pydantic](https://pydantic.dev/)
- [Typer](https://typer.tiangolo.com/)
- [Rich](https://rich.readthedocs.io/)
- [cryptography](https://cryptography.io/)

---

**Made with ❤️ for the AI community**

*Turning opaque AI runs into transparent, portable digital proofs.*
