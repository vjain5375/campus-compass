# 🚀 Quick Guide: Push to GitHub

## Step-by-Step Instructions

### Step 1: Get a Personal Access Token

1. **Go to GitHub Settings:**
   - Open: https://github.com/settings/tokens
   - Or: Click your profile picture → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Create New Token:**
   - Click "Generate new token" → "Generate new token (classic)"
   - **Note:** Give it a name like "Campus Compass"
   - **Expiration:** Choose 90 days or No expiration
   - **Select scopes:** Check the `repo` box (this gives full repository access)
   - Click "Generate token" at the bottom

3. **Copy the Token:**
   - ⚠️ **IMPORTANT:** Copy the token immediately! It looks like: `ghp_xxxxxxxxxxxxxxxxxxxx`
   - You won't be able to see it again!

### Step 2: Update Git Remote with Token

Open PowerShell in your project folder and run:

```bash
git remote set-url origin https://YOUR_TOKEN@github.com/vjain5375/campus-compass.git
```

**Replace `YOUR_TOKEN` with the token you copied!**

Example:
```bash
git remote set-url origin https://ghp_abc123xyz@github.com/vjain5375/campus-compass.git
```

### Step 3: Push to GitHub

```bash
git push -u origin main
```

That's it! Your code will be pushed to GitHub.

---

## Alternative: Use GitHub Desktop (Easier)

If the above seems complicated:

1. **Download GitHub Desktop:**
   - https://desktop.github.com/
   - Install and open it

2. **Sign in:**
   - Sign in with your `vjain5375` GitHub account

3. **Add Repository:**
   - File → Add Local Repository
   - Select your project folder: `C:\Users\vjain\Downloads\hack infinity`

4. **Push:**
   - Click "Publish repository" or "Push origin"
   - Done!

---

## Need Help?

If you get stuck, share the error message and I'll help you fix it!

