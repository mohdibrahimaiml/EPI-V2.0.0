# How a Normal User Uses EPI Recorder

**TL;DR:** Record AI API interactions, view them later, and verify their integrity.

---

## What is EPI Recorder?

Think of it as **"video recording for AI conversations"**. 

Just like you can record a video call to review later, EPI Recorder lets you record your interactions with AI (like ChatGPT) so you can:
- Debug what went wrong
- Share examples with teammates
- Keep a history of what the AI said
- Verify nothing was tampered with (cryptographic signatures)

---

## For Complete Beginners

### What You Need

1. **Python** installed on your computer
2. **An OpenAI API key** (get one from platform.openai.com)
3. **5 minutes** of your time

### Step-by-Step

#### 1. Open PowerShell (Windows)

```powershell
# Navigate to the project
cd C:\Users\dell\epi-recorder

# Activate the environment
.\venv\Scripts\activate
```

#### 2. Set Your API Key

```powershell
$env:OPENAI_API_KEY = "sk-your-key-here"
```

#### 3. Create a Test File

Create `test.py` with this code:

```python
from epi_recorder import record
import openai

with record("my_test") as session:
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Say hello!"}]
    )
    print(response.choices[0].message.content)
```

#### 4. Run It

```powershell
python test.py
```

#### 5. Check Your Recording

```powershell
# You'll see a file: my_test.epi
ls *.epi
```

**That's it!** You just recorded an AI interaction.

---

## Real-World Example: Debugging

Let's say your AI chatbot gave a weird answer. Here's how EPI helps:

### Before (without EPI):
```python
# Your code
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": user_input}]
)
# Something goes wrong... but you can't reproduce it! 😞
```

### After (with EPI):
```python
# Wrap it with EPI
with record("chatbot_session") as session:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_input}]
    )
# Now you have a recording! You can replay it, share it, analyze it! 😊
```

---

## What You Can Do

### 1. Record Conversations

```python
from epi_recorder import record
import openai

with record("conversation") as session:
    client = openai.OpenAI()
    
    # Multiple back-and-forth exchanges
    response1 = client.chat.completions.create(...)
    response2 = client.chat.completions.create(...)
    # All automatically recorded!
```

### 2. Record Streaming

```python
with record("streaming") as session:
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Tell me a story"}],
        stream=True  # Real-time streaming
    )
    
    for chunk in stream:
        print(chunk.choices[0].delta.content, end="")
```

### 3. Add Custom Notes

```python
from epi_recorder import record, get_current_session

with record("my_workflow") as session:
    # Add your own notes
    current = get_current_session()
    current.log_step("note", {"message": "Starting data processing"})
    
    # Your AI calls here
    
    current.log_step("note", {"message": "Finished successfully"})
```

---

## Viewing Recordings

### Method 1: Check the File

```powershell
# Your recording is a ZIP file
ls *.epi
```

### Method 2: CLI Viewer (if implemented)

```powershell
python -m epi_recorder.cli view my_test.epi
```

### Method 3: Extract and View JSON

```powershell
# It's just a ZIP file!
# Rename and extract:
cp my_test.epi my_test.zip
# Then extract with any ZIP tool
```

Inside you'll find:
- `manifest.json` - Overview of the recording
- `steps/` - Each API call as a separate file
- `environment.json` - Your Python version, packages, etc.
- `signature.json` - Cryptographic proof of authenticity

---

## Common Use Cases

### Use Case 1: Bug Reports

**Problem:** "The AI gave me a weird answer yesterday"

**Solution:**
```python
# Record every session
with record(f"session_{user_id}_{timestamp}") as session:
    # Your chatbot code
    pass
```

Now you can find the exact session and see what happened!

### Use Case 2: Testing

**Problem:** "I want to make sure my AI always responds correctly"

**Solution:**
```python
# In your tests
def test_ai_response():
    with record("test_response") as session:
        response = client.chat.completions.create(...)
        assert "expected text" in response.choices[0].message.content
    # Recording saved for later review
```

### Use Case 3: Cost Tracking

**Problem:** "How many tokens am I using?"

**Solution:**
```python
# Record a day's worth of API calls
with record("daily_usage") as session:
    # All your API calls
    pass

# Later: analyze the recording to see total tokens
# (The recording contains token usage for every call)
```

### Use Case 4: Compliance/Auditing

**Problem:** "I need proof of what the AI said"

**Solution:**
```python
# Record with cryptographic signature
with record("legal_consultation") as session:
    # AI consultation
    pass

# The .epi file is:
# - Cryptographically signed
# - Tamper-proof
# - Timestamp-verified
# Perfect for audits!
```

---

## FAQ

### Q: Does this slow down my code?
**A:** No! Overhead is ~1.3% (negligible)

### Q: How big are the recordings?
**A:** Typically 10-100 KB per session

### Q: Can I record without OpenAI?
**A:** Currently OpenAI only, but more providers coming soon

### Q: Is it secure?
**A:** Yes! API keys are automatically redacted from recordings

### Q: Can I edit recordings?
**A:** No, they're cryptographically signed to prevent tampering

### Q: Where are recordings saved?
**A:** In your current directory as `.epi` files

### Q: Can I share recordings?
**A:** Yes! They're just files. Send them like you would send any file.

---

## Tips & Tricks

### Tip 1: Organize by Date

```python
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
with record(f"sessions/{today}/session_{session_id}") as session:
    # Your code
    pass
```

### Tip 2: Add Context

```python
with record("customer_support") as session:
    current = get_current_session()
    current.log_step("context", {
        "customer_id": "12345",
        "issue": "billing question",
        "priority": "high"
    })
    # Your AI call
```

### Tip 3: Error Recovery

```python
try:
    with record("risky_operation") as session:
        # Risky AI call
        pass
except Exception as e:
    print(f"Error: {e}")
    print("But recording was saved! Check risky_operation.epi")
```

---

## What NOT to Do

❌ **Don't record API keys:**
```python
# BAD!
os.environ["OPENAI_API_KEY"] = "sk-123"  # Will be redacted
with record("test"):
    # But don't manually log it:
    current.log_step("key", {"api_key": "sk-123"})  # DON'T DO THIS
```

❌ **Don't commit recordings to git:**
```
# Add to .gitignore:
*.epi
```

❌ **Don't rely on recordings for real-time monitoring:**
```python
# EPI is for recording, not real-time alerts
# Use proper monitoring tools for that
```

---

## Getting Help

**Documentation:**
- Quick Start: `QUICKSTART_ACTUAL.md`
- Full Guide: `USER_GUIDE_COMPLETE.md`
- Technical Details: `COMPLETE_EPI_PROJECT_REPORT.md`

**Examples:**
```
C:\Users\dell\epi-recorder\examples\
```

**Contact:**
afridiibrahim41@gmail.com

---

## Summary

**In three lines:**

```python
from epi_recorder import record
with record("my_recording"):
    # Your OpenAI code here
```

**What you get:**
- ✅ Complete recording of AI interactions
- ✅ Timestamps and token counts
- ✅ Cryptographic verification
- ✅ Shareable .epi files
- ✅ Full replay capability

**That's it!** You're now an EPI Recorder user! 🎉

---

**Project Location:** `C:\Users\dell\epi-recorder`  
**Last Updated:** November 2, 2025  
**Version:** 1.0
