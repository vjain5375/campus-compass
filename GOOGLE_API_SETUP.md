# 🔑 How to Use Google Gemini API Key

## Quick Setup

### Step 1: Update Your .env File

Open your `.env` file and replace the content with:

```
GOOGLE_API_KEY=your_google_api_key_here
```

**Important:** Replace `your_google_api_key_here` with your actual Google API key.

### Step 2: Restart the App

The app will automatically detect and use your Google API key!

---

## Getting Your Google API Key

### Option 1: Google AI Studio (Easiest)

1. Go to: **https://aistudio.google.com/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (it looks like: `AIza...`)
5. Paste it in your `.env` file

### Option 2: Google Cloud Console

1. Go to: **https://console.cloud.google.com/**
2. Create a new project or select existing one
3. Enable the **Generative Language API**
4. Go to **APIs & Services** → **Credentials**
5. Click **"Create Credentials"** → **"API Key"**
6. Copy the key and add it to your `.env` file

---

## .env File Format

Your `.env` file should look like this:

```
GOOGLE_API_KEY=AIzaSyAbc123xyz789...
```

**No spaces, no quotes!**

---

## Benefits of Google Gemini

- ✅ **Free tier available** - Generous free usage
- ✅ **Fast responses** - Optimized for speed
- ✅ **High quality** - Great for RAG applications
- ✅ **No credit card required** for free tier

---

## Troubleshooting

### "GOOGLE_API_KEY not found"
- Make sure `.env` file is in the same folder as `app.py`
- Check the file has exactly: `GOOGLE_API_KEY=your_key`
- No spaces around the `=`

### "Invalid API key"
- Verify your key is correct
- Make sure the Generative Language API is enabled
- Check if your API key has the right permissions

### Still having issues?
- Make sure you've installed: `pip install langchain-google-genai`
- Restart the Streamlit app after updating `.env`

---

## Model Options

The app uses `gemini-pro` by default. You can also use:
- `gemini-pro` (default) - Best for most tasks
- `gemini-1.5-pro` - More advanced (if available)
- `gemini-1.5-flash` - Faster, lighter version

To change the model, edit `rag_pipeline.py` and update the `model_name` parameter.

