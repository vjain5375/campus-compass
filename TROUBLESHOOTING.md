# 🔧 Troubleshooting - App Won't Open

## Quick Fixes

### Option 1: Run the App Manually
1. Open PowerShell in this folder
2. Run this command:
   ```powershell
   python -m streamlit run app.py
   ```
3. When it asks for email, just press **Enter** (leave blank)**
4. The app should open in your browser

### Option 2: Use the Startup Script
Double-click `run_app.bat` or `run_app.ps1` in this folder

### Option 3: Check if Port is Busy
If you see "port already in use" error:
1. Close any other Streamlit apps
2. Or use a different port:
   ```powershell
   streamlit run app.py --server.port 8502
   ```
3. Then go to: http://localhost:8502

## Common Issues

### ❌ "Module not found" error
**Solution:** Make sure all dependencies are installed:
```powershell
pip install -r requirements.txt
```

### ❌ "API key not found" error
**Solution:** 
1. Check `.env` file exists
2. Make sure it has: `OPENAI_API_KEY=sk-your-key`
3. No spaces, no quotes

### ❌ Browser doesn't open automatically
**Solution:** 
1. Manually open your browser
2. Go to: http://localhost:8501
3. Or check the terminal for the exact URL

### ❌ App crashes on startup
**Solution:**
1. Check the error message in the terminal
2. Make sure Python 3.8+ is installed
3. Verify all files are in the same folder

### ❌ "Permission denied" error
**Solution:**
1. Run PowerShell as Administrator
2. Or check firewall settings

## Manual Steps

1. **Open PowerShell** in this folder:
   ```powershell
   cd "C:\Users\vjain\Downloads\hack infinity"
   ```

2. **Run the app:**
   ```powershell
   python -m streamlit run app.py
   ```

3. **Skip email prompt:**
   - Just press Enter (leave blank)

4. **Open browser manually:**
   - Go to: http://localhost:8501

## Still Not Working?

Check the terminal output for error messages and share them for help!

