# 🖥️ Where to Run EPI Commands - Visual Guide

## You're Already in the Right Place!

### **PowerShell** (Windows Terminal / Command Line)
You run these commands in the **same terminal** where you've been working.

---

## Step-by-Step Visual Guide

### 1️⃣ Open PowerShell
You have several options:

**Option A: Windows Terminal** (Recommended)
- Press `Win + X`
- Click "Windows Terminal" or "PowerShell"

**Option B: Quick Access**
- Press `Win + R`
- Type `powershell`
- Press Enter

**Option C: Start Menu**
- Click Start
- Type "PowerShell"
- Click "Windows PowerShell"

---

### 2️⃣ Navigate to Project
```powershell
cd C:\Users\dell\epi-recorder
```

You should see:
```
PS C:\Users\dell\epi-recorder>
```

---

### 3️⃣ Run Commands
Now type any EPI command:

```powershell
# List your keys
python -m epi_cli.main keys list

# Run the demo
python demo_workflow.py

# Verify a file (once you create one)
python -m epi_cli.main verify demo.epi
```

---

## 🎯 Real Example - Try This Now!

Copy and paste this into your PowerShell:

```powershell
# Make sure you're in the right directory
cd C:\Users\dell\epi-recorder

# Check if installation works
python -c "import epi_cli; print('✅ EPI is installed!')"

# List your cryptographic keys
python -m epi_cli.main keys list

# Run the demo workflow
python demo_workflow.py
```

---

## 📱 What Application?

**Answer**: You DON'T need a special application! 

| What | Where |
|------|-------|
| ✅ **PowerShell** | Built into Windows (what you're using) |
| ✅ **Command Prompt** | Also works (type `cmd` in Start) |
| ✅ **Windows Terminal** | Modern terminal (recommended) |
| ✅ **VS Code Terminal** | If you use VS Code |
| ✅ **PyCharm Terminal** | If you use PyCharm |

---

## 🎓 Understanding the Commands

### Command Structure
```powershell
python -m epi_cli.main [command] [options]
         │      │       │          │
         │      │       │          └─ Additional flags
         │      │       └─ What to do (keys, verify, view)
         │      └─ Main program entry point
         └─ Run Python module
```

### Examples with Explanations

```powershell
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Example 1: List Keys
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
python -m epi_cli.main keys list
#       │            │    │     └─ Subcommand: list
#       │            │    └─ Main command: keys
#       │            └─ Run the main program
#       └─ Use Python

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Example 2: Verify a File
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
python -m epi_cli.main verify demo.epi
#                      │      └─ File to verify
#                      └─ Command: verify

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Example 3: Record a Script
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
python -m epi_cli.main record --out demo.epi -- python demo_workflow.py
#                      │      │              │  └─ Script to record
#                      │      │              └─ Separator
#                      │      └─ Output file name
#                      └─ Command: record
```

---

## 💻 Alternative: Using VS Code

If you prefer a graphical interface:

### 1. Open VS Code
```powershell
code C:\Users\dell\epi-recorder
```

### 2. Open Terminal in VS Code
- Press `` Ctrl + ` `` (backtick)
- Or: Menu → Terminal → New Terminal

### 3. Run Commands
The terminal inside VS Code works exactly the same!

```powershell
python -m epi_cli.main keys list
```

---

## 🔧 If Commands Don't Work

### Issue 1: "python not found"
**Solution**: Use full path
```powershell
C:\Users\dell\AppData\Local\Programs\Python\Python311\python.exe -m epi_cli.main keys list
```

### Issue 2: "Module not found"
**Solution**: Reinstall
```powershell
cd C:\Users\dell\epi-recorder
pip install -e .
```

### Issue 3: "Permission denied"
**Solution**: Run as Administrator
- Right-click PowerShell → "Run as Administrator"
- Then try again

---

## 🎯 Quick Test - Try This Right Now!

### Copy this entire block and paste into PowerShell:

```powershell
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EPI Recorder Quick Test
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Write-Host "🚀 Testing EPI Recorder..." -ForegroundColor Cyan

# 1. Check Python
Write-Host "`n1️⃣ Checking Python..." -ForegroundColor Yellow
python --version

# 2. Check EPI installation
Write-Host "`n2️⃣ Checking EPI installation..." -ForegroundColor Yellow
python -c "import epi_cli; print('✅ EPI is installed!')"

# 3. List keys
Write-Host "`n3️⃣ Listing cryptographic keys..." -ForegroundColor Yellow
python -m epi_cli.main keys list

# 4. Run demo
Write-Host "`n4️⃣ Running demo workflow..." -ForegroundColor Yellow
python demo_workflow.py

Write-Host "`n✨ Test complete!" -ForegroundColor Green
```

**Just paste that entire block** and press Enter!

---

## 📊 Summary

| Question | Answer |
|----------|--------|
| **Where?** | PowerShell / Command Prompt / Terminal |
| **What application?** | No special app needed - built into Windows |
| **Which directory?** | `C:\Users\dell\epi-recorder` |
| **How to open?** | Press `Win + X` → "Terminal" or "PowerShell" |
| **Test it works?** | `python -m epi_cli.main keys list` |

---

## 🎉 You're Ready!

The commands work in:
- ✅ PowerShell (you're using this now)
- ✅ Command Prompt (cmd.exe)
- ✅ Windows Terminal (modern version)
- ✅ VS Code integrated terminal
- ✅ PyCharm terminal
- ✅ Any terminal/command line interface

**No special application needed - just your terminal!** 🚀

---

*Still confused? Just type commands in the same window where you've been working - that's PowerShell, and it's the right place!*
