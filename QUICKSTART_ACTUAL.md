# EPI Recorder - Quick Start Guide
## Get Started in 5 Minutes

**Project Location:** `C:\Users\dell\epi-recorder`

---

## Step 1: Activate Virtual Environment

```powershell
cd C:\Users\dell\epi-recorder
.\venv\Scripts\activate
```

**Verify it's working:**
```powershell
python -c "from epi_recorder import record; print('✅ Ready!')"
```

---

## Step 2: Set Your OpenAI API Key

```powershell
$env:OPENAI_API_KEY = "sk-your-api-key-here"
```

---

## Step 3: Create Your First Recording

Create a file `test_epi.py`:

```python
from epi_recorder import record
import openai

# Record an OpenAI interaction
with record("my_first_test") as session:
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "What is Python in one sentence?"}
        ]
    )
    print(response.choices[0].message.content)

print("✅ Recording saved to my_first_test.epi")
```

---

## Step 4: Run It

```powershell
python test_epi.py
```

**You should see:**
1. GPT-4's response about Python
2. Message: "✅ Recording saved to my_first_test.epi"

---

## Step 5: View Your Recording

```powershell
# Check the file exists
ls *.epi

# View it (if CLI is implemented)
python -m epi_recorder.cli view my_first_test.epi
```

---

## Common Patterns

### Pattern 1: Record Multiple Calls

```python
from epi_recorder import record
import openai

with record("conversation") as session:
    client = openai.OpenAI()
    
    # First call
    response1 = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print("Response 1:", response1.choices[0].message.content)
    
    # Second call
    response2 = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "What's 2+2?"}]
    )
    print("Response 2:", response2.choices[0].message.content)
```

### Pattern 2: Record Streaming

```python
from epi_recorder import record
import openai

with record("streaming_test") as session:
    client = openai.OpenAI()
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Count to 5"}],
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()
```

### Pattern 3: Custom Logging

```python
from epi_recorder import record, get_current_session

with record("custom_events") as session:
    # Get the session to log custom events
    current = get_current_session()
    
    # Log custom data
    current.log_step("custom.event", {
        "action": "data_loaded",
        "rows": 1000
    })
    
    # Your code here
    
    current.log_step("custom.event", {
        "action": "processing_complete",
        "success": True
    })
```

---

## Troubleshooting

### Problem: Import Error

```
ImportError: cannot import name 'record'
```

**Solution:** Make sure venv is activated
```powershell
cd C:\Users\dell\epi-recorder
.\venv\Scripts\activate
```

### Problem: No API Key

```
openai.AuthenticationError: No API key provided
```

**Solution:** Set your API key
```powershell
$env:OPENAI_API_KEY = "sk-..."
```

### Problem: Module Not Found

```
ModuleNotFoundError: No module named 'openai'
```

**Solution:** Install dependencies
```powershell
pip install openai
```

---

## What Gets Recorded?

When you use `record()`, the .epi file contains:

- ✅ All OpenAI API calls (requests and responses)
- ✅ Timestamps and duration
- ✅ Token usage statistics
- ✅ Environment information (Python version, packages)
- ✅ Custom events (if you log them)
- ✅ Cryptographic signature (for verification)

---

## Next Steps

1. **Try the examples:**
   ```powershell
   cd examples
   python basic_recording.py
   python streaming_example.py
   ```

2. **Read the full guide:**
   ```
   USER_GUIDE_COMPLETE.md
   ```

3. **Check the technical report:**
   ```
   COMPLETE_EPI_PROJECT_REPORT.md
   ```

---

## API Reference

### Main Function: `record()`

```python
from epi_recorder import record

with record(name: str, **options) as session:
    # Your code here
    pass
```

**Parameters:**
- `name` (str): Name of the recording (without .epi extension)
- `**options`: Additional configuration options

**Returns:** `EpiRecorderSession` object

### Session Methods

```python
session.log_step(kind: str, content: dict)
# Manually log a step in the recording
```

### Helper Functions

```python
from epi_recorder import get_current_session

current = get_current_session()
# Get the currently active recording session (if any)
```

---

## Complete Example

Here's a complete, copy-paste-ready example:

```python
#!/usr/bin/env python3
"""
Complete EPI Recorder Example
Demonstrates recording OpenAI interactions
"""
from epi_recorder import record, get_current_session
import openai
import os

# Set API key (or use environment variable)
# os.environ["OPENAI_API_KEY"] = "your-key-here"

def main():
    print("🎬 Starting EPI Recording Demo")
    
    with record("complete_example") as session:
        print("📝 Recording started...")
        
        # Get current session for custom logging
        current = get_current_session()
        current.log_step("demo.start", {"version": "1.0"})
        
        # Make OpenAI call
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Explain what EPI recording is in one sentence."}
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        # Print response
        answer = response.choices[0].message.content
        print(f"\n🤖 GPT-4: {answer}\n")
        
        # Log completion
        current.log_step("demo.complete", {"success": True})
        
    print("✅ Recording saved to complete_example.epi")
    print("📊 View it with: python -m epi_recorder.cli view complete_example.epi")

if __name__ == "__main__":
    main()
```

Save this as `demo.py` and run:
```powershell
python demo.py
```

---

**That's it! You're now recording AI interactions with EPI!** 🚀

**Questions?** Contact: afridiibrahim41@gmail.com
