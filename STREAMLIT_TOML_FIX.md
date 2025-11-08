# 🔧 Fix: Invalid TOML Format Error

## The Problem
Streamlit Cloud requires **TOML format** for secrets, which means string values must be in **quotes**.

## ❌ What You Have (Wrong):
```
GOOGLE_API_KEY=AIzaSyC9fGfz539RKaNwU03DUxjDPxPQL1VSVeg
```

## ✅ Correct TOML Format:
```
GOOGLE_API_KEY="AIzaSyC9fGfz539RKaNwU03DUxjDPxPQL1VSVeg"
```

## Quick Fix Steps:

1. **Clear the current text** in the Secrets editor
2. **Copy and paste this EXACT format:**
   ```
   GOOGLE_API_KEY="AIzaSyC9fGfz539RKaNwU03DUxjDPxPQL1VSVeg"
   ```
3. **Click "Save changes"**

## Important Notes:
- ✅ Use **double quotes** (`"`) around the value
- ✅ No spaces around the `=` sign
- ✅ One secret per line
- ❌ Don't use single quotes (`'`)
- ❌ Don't forget the quotes

## If You Have Multiple Secrets:
```
GOOGLE_API_KEY="AIzaSyC9fGfz539RKaNwU03DUxjDPxPQL1VSVeg"
ANOTHER_KEY="another_value"
```

Each on a new line, each with quotes around the value.

---

## Copy This:
```
GOOGLE_API_KEY="AIzaSyC9fGfz539RKaNwU03DUxjDPxPQL1VSVeg"
```

Paste it into Streamlit Cloud Secrets and click Save!

