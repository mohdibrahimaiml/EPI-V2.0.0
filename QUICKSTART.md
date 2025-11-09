# ⚡ EPI Recorder - Quick Start

## What is it?
**Cryptographically verifiable recording for AI workflows** - like Git for AI runs.

---

## 🚀 Install & Setup (1 minute)

```powershell
# 1. Install
cd C:\Users\dell\epi-recorder
pip install -e .

# 2. Generate keys (automatic on first use)
python -m epi_cli.main keys generate

# 3. Done! ✅
```

---

## 💡 Basic Usage

### Record Something
```powershell
# Record any Python script
python -m epi_cli.main record --out demo.epi -- python your_script.py

# What gets captured:
# ✅ All inputs/outputs
# ✅ API calls (redacted secrets)
# ✅ Environment info
# ✅ Cryptographic signature
```

### Verify It
```powershell
python -m epi_cli.main verify demo.epi

# Output:
# ✅ Trust Level: HIGH
# ✅ Structural: Valid
# ✅ Integrity: Verified
# ✅ Signature: Valid
```

### View It
```powershell
python -m epi_cli.main view demo.epi
# Opens interactive timeline in browser
```

---

## 📦 What Gets Captured?

| Category | Examples |
|----------|----------|
| 🤖 **AI Calls** | GPT-4, Claude, prompts, responses |
| 🔒 **Security** | Auto-redacts API keys, tokens |
| 📁 **Files** | Inputs, outputs, artifacts |
| 🖥️ **Environment** | OS, Python, packages |
| ✅ **Signature** | Ed25519 cryptographic proof |

---

## 🎯 Common Use Cases

### 1. Research Reproducibility
```powershell
epi record --out experiment.epi -- python train.py
# Share .epi with reviewers for exact reproduction
```

### 2. Bug Reports
```powershell
epi record --out bug.epi -- pytest failing_test.py
# Send .epi to developer - includes exact environment
```

### 3. Compliance & Auditing
```powershell
epi record --out prod_run.epi -- python ai_decision.py
# Tamper-proof audit trail for regulators
```

### 4. CI/CD Integration
```powershell
epi record --out test.epi -- pytest tests/
epi verify test.epi --json > results.json
```

---

## 🔑 Key Management

```powershell
# List keys
python -m epi_cli.main keys list

# Generate new key
python -m epi_cli.main keys generate --name mykey

# Export public key (for sharing)
python -m epi_cli.main keys export --name mykey
```

Keys stored at: `C:\Users\dell\.epi\keys\`

---

## 🔐 Security Features

✅ **Auto-redacts 15+ secret patterns**:
- OpenAI keys (`sk-...`)
- AWS credentials (`AKIA...`)
- Bearer tokens
- JWT tokens
- Passwords

✅ **Tamper-proof**: Any modification breaks signature

✅ **Cryptographic**: Ed25519 + SHA-256

---

## 📊 File Format

```
demo.epi (ZIP archive)
├── mimetype                 # Format identifier
├── manifest.json            # Metadata + signature
├── content/                 # Recorded steps
│   └── step_*.json
└── viewer/                  # Self-contained HTML viewer
    └── index.html
```

---

## 🎓 Try the Demo

```powershell
# Run demo workflow
python demo_workflow.py

# See what happened
cat demo_output.json

# Now imagine recording this with EPI:
# python -m epi_cli.main record --out demo.epi -- python demo_workflow.py
```

---

## 📚 Full Documentation

- **Usage Guide**: `USAGE_GUIDE.md` - Complete how-to
- **Coverage Report**: `COVERAGE_REPORT.md` - Test details
- **README**: `README.md` - Project overview

---

## 💬 Key Commands Cheat Sheet

| Command | What it does |
|---------|--------------|
| `record --out X.epi -- cmd` | Record command execution |
| `verify X.epi` | Verify integrity & signature |
| `view X.epi` | Open in browser |
| `keys list` | Show all keypairs |
| `keys generate --name N` | Create new keypair |
| `keys export --name N` | Export public key |

---

## 🆘 Need Help?

**Common Issues**:

1. **"ModuleNotFoundError"**
   ```powershell
   pip install -e .
   ```

2. **"Keys not found"**
   ```powershell
   python -m epi_cli.main keys generate
   ```

3. **More help**: See `USAGE_GUIDE.md`

---

## ✨ What Makes EPI Special?

| Feature | Benefit |
|---------|---------|
| 🎁 **Single File** | Everything in one `.epi` - share easily |
| 🔒 **Secure** | Auto-redacts secrets, cryptographic proof |
| 👁️ **Viewable** | Beautiful HTML viewer embedded |
| ♻️ **Reproducible** | Exact environment capture |
| 🚀 **Zero Config** | Works out of the box |

---

**Ready to record your first AI workflow?**

```powershell
python -m epi_cli.main record --out my_first.epi -- python your_script.py
```

🎉 **You're now using EPI Recorder!**
