# 🚀 GitHub Setup Instructions

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `campus-compass` (or any name you prefer)
3. Description: "AI-powered chatbot for college queries using RAG"
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **"Create repository"**

## Step 2: Connect and Push

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/campus-compass.git

# Rename main branch if needed
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 3: Verify

1. Go to your GitHub repository
2. Check that all files are uploaded
3. Make sure `.env` file is **NOT** visible (it's in .gitignore)

## Important Notes

✅ **What's included:**
- All Python code files
- Requirements.txt
- README.md
- Documentation files
- .gitignore

❌ **What's NOT included (protected by .gitignore):**
- `.env` file (your API keys)
- `vector_db/` folder (database files)
- `.venv/` folder (virtual environment)
- `__pycache__/` folders
- Personal documents

## Next Steps

After pushing to GitHub, you can:
- Share the repository with others
- Deploy to Streamlit Cloud (if public)
- Collaborate with team members
- Track issues and improvements

## Deploy to Streamlit Cloud (Optional)

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Connect your GitHub repository
4. Set main file: `app.py`
5. Add secrets: `GOOGLE_API_KEY` = your API key
6. Deploy!

---

**Security Reminder:** Never commit your `.env` file or API keys to GitHub!

