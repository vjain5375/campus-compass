# 🔐 Streamlit Cloud Secrets - Correct Format

## Error: "Invalid format: please enter valid TOML"

This error occurs when entering secrets in Streamlit Cloud. Here's the correct format:

## ✅ Correct Format for Streamlit Cloud Secrets

When adding secrets in Streamlit Cloud Settings → Secrets, use this format:

```
GOOGLE_API_KEY=AIzaSyC9fGfz539RKaNwU03DUxjDPxPQLlVSVeg
```

**Important:**
- ✅ Use `KEY=VALUE` format (no spaces around `=`)
- ✅ No quotes needed
- ✅ One secret per line
- ✅ No empty lines

## ❌ Common Mistakes (Don't Do This)

```
❌ GOOGLE_API_KEY = "your_key"     (spaces around =, quotes)
❌ GOOGLE_API_KEY="your_key"       (quotes not needed)
❌ GOOGLE_API_KEY: your_key        (wrong separator)
❌ [secrets]                       (don't use TOML headers)
   GOOGLE_API_KEY = "your_key"
```

## ✅ Step-by-Step in Streamlit Cloud

1. Go to your app on Streamlit Cloud
2. Click **"Settings"** (gear icon) → **"Secrets"**
3. In the secrets editor, enter:
   ```
   GOOGLE_API_KEY=AIzaSyC9fGfz539RKaNwU03DUxjDPxPQLlVSVeg
   ```
4. Click **"Save"**
5. The app will automatically restart

## Example: Multiple Secrets (if needed)

If you need multiple secrets:
```
GOOGLE_API_KEY=AIzaSyC9fGfz539RKaNwU03DUxjDPxPQLlVSVeg
ANOTHER_KEY=another_value
THIRD_KEY=third_value
```

Each on a new line, no empty lines between them.

## Verify It Works

After saving, check the app logs to ensure:
- No TOML format errors
- API key is loaded correctly
- App starts without errors

---

## Quick Fix

Just copy and paste this into Streamlit Cloud Secrets:
```
GOOGLE_API_KEY=AIzaSyC9fGfz539RKaNwU03DUxjDPxPQLlVSVeg
```

Replace with your actual API key if different!

