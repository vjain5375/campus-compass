# 🔧 Troubleshooting localhost Issues

## Quick Fixes

### 1. Check if App is Running
Open your browser and try:
- http://localhost:8501
- http://127.0.0.1:8501

### 2. If Port is Busy
If port 8501 is already in use, try a different port:
```bash
streamlit run app.py --server.port 8502
```
Then open: http://localhost:8502

### 3. Stop and Restart
If the app is stuck:
1. **Stop the current process:**
   - Press `Ctrl+C` in the terminal where Streamlit is running
   - Or close the terminal window

2. **Kill stuck processes (Windows):**
   ```powershell
   taskkill /F /IM streamlit.exe
   taskkill /F /IM python.exe
   ```

3. **Restart the app:**
   ```bash
   streamlit run app.py
   ```

### 4. Check for Errors
Look at the terminal output for error messages. Common issues:
- **Import errors:** Missing dependencies - run `pip install -r requirements.txt`
- **API key errors:** Check your `.env` file has `GOOGLE_API_KEY=...`
- **Port already in use:** Use a different port (see #2)

### 5. Clear Browser Cache
Sometimes browser cache causes issues:
- Press `Ctrl+Shift+R` (hard refresh)
- Or clear browser cache and try again

### 6. Check Firewall
Windows Firewall might be blocking:
1. Go to Windows Security → Firewall
2. Allow Python/Streamlit through firewall

### 7. Try Different Browser
Sometimes browser-specific issues occur:
- Try Chrome, Firefox, or Edge

## Common Error Messages

### "Address already in use"
**Solution:** Port 8501 is busy. Use a different port:
```bash
streamlit run app.py --server.port 8502
```

### "ModuleNotFoundError"
**Solution:** Install missing dependencies:
```bash
pip install -r requirements.txt
```

### "API key not found"
**Solution:** Check your `.env` file exists and has:
```
GOOGLE_API_KEY=your_key_here
```

### "Connection refused"
**Solution:** 
1. Make sure Streamlit is actually running
2. Check terminal for errors
3. Try restarting the app

## Still Not Working?

1. **Check terminal output** - Look for error messages
2. **Verify virtual environment** - Make sure you're in `.venv`
3. **Reinstall dependencies:**
   ```bash
   pip install --upgrade streamlit
   pip install -r requirements.txt
   ```

4. **Check file paths** - Make sure you're in the project directory

## Quick Restart Command
```bash
# Stop all Streamlit processes
taskkill /F /IM streamlit.exe 2>$null

# Start fresh
streamlit run app.py
```

