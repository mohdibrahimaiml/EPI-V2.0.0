# EPI Recorder - Complete User Guide
## How to Use the EPI Project from Start to Finish

**Project Location:** `C:\Users\dell\epi-recorder`  
**Current Status:** Production-ready Python package  
**Contact:** afridiibrahim41@gmail.com

---

## TABLE OF CONTENTS

1. [Quick Start (5 Minutes)](#quick-start-5-minutes)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [Recording Scenarios](#recording-scenarios)
5. [Viewing Recordings](#viewing-recordings)
6. [CLI Commands](#cli-commands)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)
9. [Examples Library](#examples-library)

---

## QUICK START (5 Minutes)

### Step 1: Activate Virtual Environment

```powershell
# Windows PowerShell
cd C:\Users\dell\epi-recorder
.\venv\Scripts\activate
```

```bash
# Linux/Mac
cd /path/to/epi-recorder
source venv/bin/activate
```

### Step 2: Your First Recording

Create a file `my_first_recording.py`:

```python
from epi_recorder import record
import openai
import os

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Record an interaction
with record("my_first_recording") as session:
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "What is Python?"}
        ]
    )
    print(response.choices[0].message.content)

print("✅ Recording saved to my_first_recording.epi")
```

### Step 3: Run It

```powershell
python my_first_recording.py
```

**Expected Output:**
```
[GPT-4 response about Python]
✅ Recording saved to my_first_recording.epi
```

### Step 4: View Your Recording

```powershell
python -m epi_recorder.cli view my_first_recording.epi
```

**That's it!** You just recorded and viewed your first AI interaction.

---

## INSTALLATION

### Method 1: Use Existing Installation (Recommended)

The package is already installed in the virtual environment:

```powershell
cd C:\Users\dell\epi-recorder
.\venv\Scripts\activate
```

**Verify installation:**
```powershell
python -c "from epi_recorder import record; print('✅ EPI Recorder ready!')"
```

### Method 2: Install from Source

```powershell
# Clone or navigate to the project
cd C:\Users\dell\epi-recorder

# Create virtual environment
python -m venv venv

# Activate
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install in development mode
pip install -e .

# Install dependencies
pip install openai cryptography
```

### Method 3: Install from PyPI (When Published)

```bash
pip install epi-recorder
```

---

## BASIC USAGE

### 1. Simple Recording

```python
from epi_recorder import record
import openai

with record("output") as session:
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(response.choices[0].message.content)
```

**What gets recorded:**
- ✅ Your request (model, messages, parameters)
- ✅ OpenAI's response (content, tokens used)
- ✅ Timing information (duration, timestamps)
- ✅ Environment details (Python version, packages)
- ✅ Cryptographic signature (for verification)

### 2. Without Auto-Patching

If you want manual control:

```python
from epi_recorder import Recorder

with Recorder("output.epi", auto_patch_openai=False) as rec:
    # Manually log steps
    rec.log_step("custom.event", {
        "data": "your data here"
    })
```

### 3. Environment Variables

**Set your API key securely:**

```powershell
# PowerShell
$env:OPENAI_API_KEY = "sk-..."

# Bash
export OPENAI_API_KEY="sk-..."
```

**Important:** EPI Recorder automatically redacts sensitive environment variables in recordings!

---

## RECORDING SCENARIOS

### Scenario 1: Basic Chat Completion

```python
# examples/basic_recording.py
from epi_recorder import Recorder
import openai

with Recorder("basic_example.epi") as rec:
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ],
        temperature=0.7,
        max_tokens=150
    )
    print(response.choices[0].message.content)
```

**Use Case:** Documentation, debugging, testing

### Scenario 2: Streaming Response

```python
# examples/streaming_example.py
from epi_recorder import Recorder
import openai

with Recorder("streaming_example.epi") as rec:
    client = openai.OpenAI()
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Write a haiku about coding"}],
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()
```

**What's captured:**
- ✅ Each streaming chunk
- ✅ Token-by-token timing
- ✅ Complete reconstruction of response

**Use Case:** Real-time interaction analysis, performance testing

### Scenario 3: Multi-Turn Conversation

```python
# examples/multi_turn_conversation.py
from epi_recorder import Recorder
import openai

with Recorder("conversation.epi") as rec:
    client = openai.OpenAI()
    messages = []
    
    # Turn 1
    messages.append({"role": "user", "content": "What's the weather like?"})
    response1 = client.chat.completions.create(model="gpt-4", messages=messages)
    messages.append({"role": "assistant", "content": response1.choices[0].message.content})
    print(f"Turn 1: {response1.choices[0].message.content}")
    
    # Turn 2
    messages.append({"role": "user", "content": "Should I bring an umbrella?"})
    response2 = client.chat.completions.create(model="gpt-4", messages=messages)
    messages.append({"role": "assistant", "content": response2.choices[0].message.content})
    print(f"Turn 2: {response2.choices[0].message.content}")
    
    # Turn 3
    messages.append({"role": "user", "content": "What about a raincoat?"})
    response3 = client.chat.completions.create(model="gpt-4", messages=messages)
    print(f"Turn 3: {response3.choices[0].message.content}")
```

**Use Case:** Chatbot development, context analysis

### Scenario 4: Error Handling

```python
# examples/error_handling.py
from epi_recorder import Recorder
import openai

try:
    with Recorder("error_example.epi") as rec:
        client = openai.OpenAI(api_key="invalid")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}]
        )
except Exception as e:
    print(f"❌ Error occurred: {e}")
    print("✅ Recording saved despite error!")
```

**Key Feature:** Recordings are saved even when errors occur!

**Use Case:** Debugging failures, QA testing

### Scenario 5: Concurrent Recordings (Multi-Threading)

```python
# examples/concurrent_recordings.py
from epi_recorder import Recorder
import openai
import threading

def record_thread(thread_id):
    with Recorder(f"thread_{thread_id}.epi") as rec:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Hello from thread {thread_id}"}]
        )
        print(f"Thread {thread_id}: {response.choices[0].message.content}")

# Create 5 threads
threads = [
    threading.Thread(target=record_thread, args=(i,))
    for i in range(5)
]

# Start all threads
for t in threads:
    t.start()

# Wait for completion
for t in threads:
    t.join()

print("✅ All threads complete, 5 separate recordings created!")
```

**Use Case:** Load testing, parallel workflows

---

## VIEWING RECORDINGS

### Method 1: CLI Viewer (Terminal)

```powershell
python -m epi_recorder.cli view my_recording.epi
```

**Output:**
```
📦 EPI Recording: my_recording.epi

Session ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
Duration: 2.45 seconds
Steps: 3

┌─ Step 1: session.start ──────────────────────┐
│ Timestamp: 2025-01-24T10:30:00.000Z          │
│ Session ID: a1b2c3d4-e5f6-7890-abcd...       │
└───────────────────────────────────────────────┘

┌─ Step 2: llm.request ─────────────────────────┐
│ Provider: openai                               │
│ Model: gpt-4                                   │
│ Messages:                                      │
│   [user]: "What is Python?"                    │
└───────────────────────────────────────────────┘

┌─ Step 3: llm.response ────────────────────────┐
│ Content: "Python is a high-level..."          │
│ Tokens: 150                                    │
└───────────────────────────────────────────────┘
```

### Method 2: Web Viewer (Static HTML)

```powershell
# Copy the viewer to your project
cp epi_viewer_static/index.html ./viewer.html

# Open in browser
start viewer.html  # Windows
# open viewer.html   # Mac
# xdg-open viewer.html  # Linux
```

**Then drag and drop your `.epi` file onto the viewer!**

**Features:**
- 📊 Visual timeline
- 🔍 Token-by-token replay
- 📈 Performance graphs
- 🔄 Request/response diff

### Method 3: Programmatic Access

```python
from epi_recorder.packaging import load_epi_archive

# Load recording
manifest, steps, environment, signature = load_epi_archive("my_recording.epi")

# Analyze
print(f"Session ID: {manifest['session_id']}")
print(f"Duration: {manifest['metadata']['duration']} seconds")
print(f"Steps: {len(steps)}")

for step in steps:
    print(f"- {step['kind']}: {step['timestamp']}")
```

---

## CLI COMMANDS

### Full Command Reference

```powershell
# View recording
python -m epi_recorder.cli view <file.epi>

# Validate recording
python -m epi_recorder.cli check <file.epi>

# Verify signature
python -m epi_recorder.cli verify <file.epi>

# Generate signing key
python -m epi_recorder.cli keygen

# Export to JSON
python -m epi_recorder.cli export <file.epi> --format json

# Compare two recordings
python -m epi_recorder.cli diff <file1.epi> <file2.epi>

# Show version
python -m epi_recorder.cli version
```

### Detailed Examples

#### 1. View Recording

```powershell
python -m epi_recorder.cli view my_recording.epi
```

**Options:**
```
--verbose    Show full details
--json       Output as JSON
--steps      Show only steps
```

#### 2. Check Recording Integrity

```powershell
python -m epi_recorder.cli check my_recording.epi
```

**Checks:**
- ✅ ZIP file valid
- ✅ Manifest present
- ✅ All referenced files exist
- ✅ File hashes match
- ✅ Signature valid

#### 3. Verify Signature

```powershell
python -m epi_recorder.cli verify my_recording.epi
```

**Output:**
```
✅ Signature valid
   Algorithm: Ed25519
   Signed by: abc123...def456
   All file hashes verified
```

#### 4. Generate Signing Key

```powershell
python -m epi_recorder.cli keygen
```

**Creates:** `~/.epi/signing_key.pem`

**Output:**
```
✅ Key pair generated
   Private key: C:\Users\dell\.epi\signing_key.pem
   Keep this file secure!
```

#### 5. Export Recording

```powershell
python -m epi_recorder.cli export my_recording.epi --format json > output.json
```

**Formats supported:**
- `json` - Complete JSON export
- `csv` - Tabular step data
- `markdown` - Human-readable report

#### 6. Compare Recordings

```powershell
python -m epi_recorder.cli diff recording1.epi recording2.epi
```

**Shows:**
- Model differences
- Token usage changes
- Response variations
- Performance deltas

---

## ADVANCED FEATURES

### 1. Custom Signing Key

```python
from epi_recorder import Recorder

with Recorder("output.epi", signing_key_path="my_key.pem") as rec:
    # Your code here
    pass
```

### 2. Disable Signing

```python
from epi_recorder import Recorder

with Recorder("output.epi", sign=False) as rec:
    # Unsigned recording (not recommended for production)
    pass
```

### 3. Custom Metadata

```python
from epi_recorder import Recorder

with Recorder("output.epi") as rec:
    rec.metadata["project"] = "My Project"
    rec.metadata["version"] = "1.0.0"
    rec.metadata["author"] = "Your Name"
    
    # Your code here
```

### 4. Exclude Environment Variables

```python
from epi_recorder import Recorder

with Recorder("output.epi", capture_env_vars=False) as rec:
    # Environment variables not captured
    pass
```

### 5. Custom Step Logging

```python
from epi_recorder import Recorder

with Recorder("output.epi") as rec:
    # Log custom events
    rec.log_step("data.loaded", {
        "source": "database",
        "rows": 1000
    })
    
    rec.log_step("processing.start", {
        "algorithm": "transformer"
    })
    
    # ... do work ...
    
    rec.log_step("processing.complete", {
        "duration": 5.2,
        "success": True
    })
```

### 6. Nested Recorders

```python
from epi_recorder import Recorder

with Recorder("outer.epi") as rec1:
    # Outer recording
    
    with Recorder("inner.epi") as rec2:
        # Inner recording (separate file)
        pass
    
    # Back to outer recording
```

---

## TROUBLESHOOTING

### Problem 1: Import Error

**Error:**
```
ImportError: No module named 'epi_recorder'
```

**Solution:**
```powershell
# Activate virtual environment
cd C:\Users\dell\epi-recorder
.\venv\Scripts\activate

# Verify installation
pip list | Select-String epi
```

### Problem 2: OpenAI API Key Not Set

**Error:**
```
openai.AuthenticationError: No API key provided
```

**Solution:**
```powershell
$env:OPENAI_API_KEY = "sk-your-key-here"
```

### Problem 3: Permission Denied (Signing Key)

**Error:**
```
PermissionError: Cannot write to C:\Users\dell\.epi\signing_key.pem
```

**Solution:**
```powershell
# Create directory manually
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.epi"

# Or specify custom location
python -m epi_recorder.cli keygen --output my_key.pem
```

### Problem 4: Unicode Encoding Error (Windows)

**Error:**
```
UnicodeEncodeError: 'charmap' codec can't encode character
```

**Solution:**
```powershell
# Set UTF-8 encoding
$env:PYTHONIOENCODING = "utf-8"

# Or in Python code
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

### Problem 5: Recording File Not Created

**Check:**
```python
import os
print(os.path.exists("my_recording.epi"))
print(os.getcwd())  # Verify current directory
```

**Common causes:**
- Exception before context exit
- Wrong directory
- Permission issues

**Solution:**
```python
from pathlib import Path

output_path = Path.home() / "recordings" / "my_recording.epi"
output_path.parent.mkdir(parents=True, exist_ok=True)

with Recorder(str(output_path)) as rec:
    # Your code
    pass
```

### Problem 6: Old OpenAI SDK Version

**Error:**
```
AttributeError: module 'openai' has no attribute 'OpenAI'
```

**Solution:**
```powershell
pip install --upgrade openai>=1.0.0
```

---

## EXAMPLES LIBRARY

### Available Examples (in `examples/` folder)

1. **basic_recording.py** - Simple chat completion
2. **streaming_example.py** - Real-time streaming
3. **multi_turn_conversation.py** - Context-aware chat
4. **error_handling.py** - Exception handling
5. **concurrent_recordings.py** - Multi-threaded recording

### Running Examples

```powershell
cd C:\Users\dell\epi-recorder

# Activate venv
.\venv\Scripts\activate

# Set API key
$env:OPENAI_API_KEY = "your-key-here"

# Run any example
python examples/basic_recording.py
python examples/streaming_example.py
python examples/multi_turn_conversation.py
```

### Example Output Locations

All examples save recordings in the current directory:
```
basic_example.epi
streaming_example.epi
conversation.epi
error_example.epi
thread_0.epi, thread_1.epi, ...
```

---

## COMPLETE WORKFLOW EXAMPLE

### Step-by-Step: From Recording to Analysis

#### 1. Record an Interaction

```python
# my_workflow.py
from epi_recorder import Recorder
import openai
import os

os.environ["OPENAI_API_KEY"] = "your-key-here"

with Recorder("my_workflow.epi") as rec:
    client = openai.OpenAI()
    
    # First request
    response1 = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Explain recursion"}]
    )
    print("Response 1:", response1.choices[0].message.content)
    
    # Second request
    response2 = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Give me a recursive example in Python"}]
    )
    print("Response 2:", response2.choices[0].message.content)

print("✅ Workflow recorded to my_workflow.epi")
```

#### 2. Run the Recording

```powershell
python my_workflow.py
```

#### 3. Verify the Recording

```powershell
python -m epi_recorder.cli check my_workflow.epi
```

**Output:**
```
✅ Recording valid
   File size: 15.3 KB
   Steps: 5
   Duration: 3.2 seconds
   Signature: Valid
```

#### 4. View the Recording

```powershell
python -m epi_recorder.cli view my_workflow.epi
```

#### 5. Export for Analysis

```powershell
python -m epi_recorder.cli export my_workflow.epi --format json > analysis.json
```

#### 6. Analyze Programmatically

```python
import json

with open("analysis.json") as f:
    data = json.load(f)

# Calculate total tokens
total_tokens = sum(
    step["content"].get("usage", {}).get("total_tokens", 0)
    for step in data["steps"]
    if step["kind"] == "llm.response"
)

print(f"Total tokens used: {total_tokens}")
```

---

## BEST PRACTICES

### 1. Security

✅ **Do:**
- Use environment variables for API keys
- Keep signing keys private
- Review recordings before sharing

❌ **Don't:**
- Hardcode API keys in code
- Commit `.pem` files to git
- Share signed recordings publicly without verification

### 2. Organization

**Recommended folder structure:**
```
my_project/
├── recordings/          # All .epi files
│   ├── 2025-01-24/
│   │   ├── test_001.epi
│   │   └── test_002.epi
│   └── 2025-01-25/
├── scripts/             # Recording scripts
└── analysis/            # Exported data
```

### 3. Naming Conventions

**Good:**
```
test_login_flow_2025-01-24.epi
prod_api_call_v1.2.3.epi
debug_streaming_issue_123.epi
```

**Bad:**
```
recording.epi
test.epi
output.epi
```

### 4. Version Control

**.gitignore:**
```
# EPI recordings (usually large)
*.epi

# API keys
.env
*.pem

# Virtual environment
venv/
```

**Exception:** Small example recordings can be committed for documentation.

---

## INTEGRATION EXAMPLES

### With Pytest

```python
# test_with_epi.py
import pytest
from epi_recorder import Recorder
import openai

def test_openai_integration():
    with Recorder("test_integration.epi") as rec:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}]
        )
        assert response.choices[0].message.content
    
    # Verify recording was created
    assert Path("test_integration.epi").exists()
```

### With FastAPI

```python
# main.py
from fastapi import FastAPI
from epi_recorder import Recorder
import openai

app = FastAPI()

@app.post("/chat")
async def chat(message: str):
    with Recorder(f"api_call_{message[:10]}.epi") as rec:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message}]
        )
        return {"response": response.choices[0].message.content}
```

### With Jupyter Notebook

```python
# In Jupyter cell
from epi_recorder import Recorder
import openai

# Record throughout notebook session
recorder = Recorder("notebook_session.epi")
recorder.__enter__()

# ... your notebook cells ...

# At the end
recorder.__exit__(None, None, None)
print("✅ Notebook session recorded!")
```

---

## PERFORMANCE TIPS

### 1. Minimize Recording Overhead

**Overhead:** ~1.3% (negligible for most use cases)

**If you need maximum performance:**
```python
# Only record specific sections
def critical_section():
    # Fast code (not recorded)
    pass

with Recorder("important_part.epi") as rec:
    # Only this part is recorded
    result = important_function()
```

### 2. Batch Processing

```python
from epi_recorder import Recorder

# Record entire batch in one session
with Recorder("batch_job.epi") as rec:
    for item in large_dataset:
        process_item(item)  # All items in one recording
```

### 3. Streaming Mode

For long-running processes:
```python
# Coming soon: streaming mode
with Recorder("streaming.epi", mode="streaming") as rec:
    # Steps flushed to disk immediately
    # Lower memory usage
    pass
```

---

## NEXT STEPS

### For Beginners

1. ✅ Run the Quick Start example
2. ✅ Try `examples/basic_recording.py`
3. ✅ View a recording with CLI
4. ✅ Experiment with streaming

### For Developers

1. ✅ Integrate into your project
2. ✅ Add to test suite
3. ✅ Create custom logging steps
4. ✅ Build analysis tools

### For Advanced Users

1. ✅ Multi-threaded recordings
2. ✅ Custom signing keys
3. ✅ Programmatic analysis
4. ✅ CI/CD integration

---

## SUPPORT & RESOURCES

### Documentation

- **This Guide:** `USER_GUIDE_COMPLETE.md`
- **Quick Start:** `QUICKSTART.md`
- **Technical Report:** `COMPLETE_EPI_PROJECT_REPORT.md`
- **API Reference:** `docs/API.md`

### Example Code

```
C:\Users\dell\epi-recorder\examples\
```

### Getting Help

**Email:** afridiibrahim41@gmail.com

**Include in bug reports:**
1. Python version: `python --version`
2. EPI Recorder version: `pip show epi-recorder`
3. Error message (full traceback)
4. Minimal reproduction code

### Contributing

1. Fork the repository
2. Create feature branch
3. Add tests
4. Submit pull request

---

## APPENDIX

### A. File Locations

**Project Root:**
```
C:\Users\dell\epi-recorder
```

**Virtual Environment:**
```
C:\Users\dell\epi-recorder\venv
```

**Signing Key (default):**
```
C:\Users\dell\.epi\signing_key.pem
```

**Examples:**
```
C:\Users\dell\epi-recorder\examples\
```

**Tests:**
```
C:\Users\dell\epi-recorder\tests\
```

### B. System Requirements

- **Python:** 3.8 or higher
- **Operating System:** Windows, macOS, Linux
- **Dependencies:**
  - openai >= 1.0.0
  - cryptography >= 41.0.0

### C. Package Size

- **Source:** ~50 KB
- **With dependencies:** ~5 MB
- **Typical recording:** 10-100 KB

### D. Performance Metrics

- **Recording overhead:** 1.3%
- **Startup time:** <100ms
- **Memory usage:** <5 MB per recording
- **Max recording size:** Limited by disk space

---

**Last Updated:** November 2, 2025  
**Version:** 1.0  
**Status:** Production Ready  
**Project:** EPI Recorder - Extended Prompt Interaction Recording System

---

## SUMMARY

**What You Learned:**

1. ✅ How to install and set up EPI Recorder
2. ✅ How to record AI interactions (basic, streaming, multi-turn)
3. ✅ How to view and analyze recordings
4. ✅ How to use CLI commands
5. ✅ Advanced features (signing, custom metadata, threading)
6. ✅ Troubleshooting common issues
7. ✅ Integration with other tools
8. ✅ Best practices and tips

**Quick Reference Card:**

```python
# Record
from epi_recorder import record
with record("filename") as session:
    # your code here
    pass

# View
python -m epi_recorder.cli view filename.epi

# Verify
python -m epi_recorder.cli verify filename.epi
```

**You're ready to use EPI Recorder in your projects!** 🚀
