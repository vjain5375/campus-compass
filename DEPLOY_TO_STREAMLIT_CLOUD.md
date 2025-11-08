# 🚀 Deploy to Streamlit Cloud (Correct Platform)

## Why Not Vercel?
- ❌ Vercel is for static sites and serverless functions
- ❌ Streamlit needs a Python runtime environment
- ✅ Streamlit Cloud is specifically designed for Streamlit apps

## Step-by-Step Deployment to Streamlit Cloud

### Step 1: Prepare Your Repository
Your code is already on GitHub at: `vjain5375/campus-compass`

### Step 2: Go to Streamlit Cloud
1. Visit: **https://share.streamlit.io/**
2. Sign in with your **GitHub account** (same account: `vjain5375`)

### Step 3: Deploy Your App
1. Click **"New app"** button
2. Fill in the details:
   - **Repository:** `vjain5375/campus-compass`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** (auto-generated, e.g., `campus-compass-vjain5375.streamlit.app`)

3. Click **"Deploy"**

### Step 4: Add Secrets (API Key)
1. After deployment starts, go to **"Settings"** (gear icon)
2. Click **"Secrets"** tab
3. Add your Google API key:
   ```
   GOOGLE_API_KEY=AIzaSyC9fGfz539RKaNwU03DUxjDPxPQLlVSVeg
   ```
   (Or use your actual API key)

4. Click **"Save"**

### Step 5: Wait for Deployment
- Streamlit Cloud will automatically:
  - Install dependencies from `requirements.txt`
  - Start your app
  - Make it publicly accessible

### Step 6: Access Your App
Your app will be live at:
```
https://campus-compass-vjain5375.streamlit.app
```
(URL will be shown after deployment)

---

## Alternative: Deploy to Other Platforms

### Option 2: Railway
1. Go to: https://railway.app/
2. Sign in with GitHub
3. New Project → Deploy from GitHub
4. Select your repository
5. Add environment variable: `GOOGLE_API_KEY`

### Option 3: Render
1. Go to: https://render.com/
2. Sign in with GitHub
3. New → Web Service
4. Connect your repository
5. Build command: `pip install -r requirements.txt`
6. Start command: `streamlit run app.py`
7. Add environment variable: `GOOGLE_API_KEY`

### Option 4: Heroku
1. Go to: https://www.heroku.com/
2. Create account
3. Create new app
4. Connect GitHub repository
5. Add `GOOGLE_API_KEY` in Config Vars
6. Deploy

---

## Recommended: Streamlit Cloud
✅ **Free** for public repositories  
✅ **Automatic deployments** from GitHub  
✅ **Built specifically for Streamlit**  
✅ **Easy secrets management**  
✅ **No credit card required**

---

## Quick Deploy Command (Streamlit Cloud)
Just go to: https://share.streamlit.io/ and follow the steps above!

Your app will be live in 2-3 minutes! 🚀

