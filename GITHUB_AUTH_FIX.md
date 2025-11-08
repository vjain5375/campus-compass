# 🔐 GitHub Authentication Fix

## Issue
Git is trying to use a different GitHub account (`urjasangamrgipt`) than your repository owner (`vjain5375`).

## Solution Options

### Option 1: Use Personal Access Token (Recommended)

1. **Create a Personal Access Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Name it: "Campus Compass"
   - Select scopes: `repo` (full control of private repositories)
   - Click "Generate token"
   - **Copy the token immediately** (you won't see it again!)

2. **Update remote URL with token:**
   ```bash
   git remote set-url origin https://YOUR_TOKEN@github.com/vjain5375/campus-compass.git
   ```

3. **Push again:**
   ```bash
   git push -u origin main
   ```

### Option 2: Use SSH (More Secure)

1. **Check if you have SSH key:**
   ```bash
   ls ~/.ssh
   ```

2. **If no SSH key, generate one:**
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

3. **Add SSH key to GitHub:**
   - Copy your public key: `cat ~/.ssh/id_ed25519.pub`
   - Go to: https://github.com/settings/keys
   - Click "New SSH key"
   - Paste your key and save

4. **Change remote to SSH:**
   ```bash
   git remote set-url origin git@github.com:vjain5375/campus-compass.git
   ```

5. **Push:**
   ```bash
   git push -u origin main
   ```

### Option 3: Use GitHub Desktop

1. Download GitHub Desktop: https://desktop.github.com/
2. Sign in with your `vjain5375` account
3. Add the repository
4. Push from the GUI

### Option 4: Clear Credentials and Re-authenticate

1. **Clear stored credentials:**
   ```bash
   git credential-manager-core erase
   ```
   Or on Windows:
   ```bash
   cmdkey /list
   cmdkey /delete:git:https://github.com
   ```

2. **Try pushing again** - it will prompt for credentials:
   ```bash
   git push -u origin main
   ```
   - Username: `vjain5375`
   - Password: Use your Personal Access Token (not your GitHub password)

## Quick Fix (Easiest)

If you just want to push quickly:

1. Get a Personal Access Token from: https://github.com/settings/tokens
2. Run:
   ```bash
   git remote set-url origin https://YOUR_TOKEN@github.com/vjain5375/campus-compass.git
   git push -u origin main
   ```

Replace `YOUR_TOKEN` with your actual token.

---

**Note:** Never share your Personal Access Token publicly!

