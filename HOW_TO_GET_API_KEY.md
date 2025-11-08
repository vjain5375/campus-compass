# 🔑 How to Get Your OpenAI API Key

## Step-by-Step Guide

### Step 1: Go to OpenAI's Website
1. Open your web browser
2. Go to: **https://platform.openai.com/api-keys**
   - Or visit: https://platform.openai.com and click on "API" → "API Keys"

### Step 2: Sign In or Create Account
1. If you already have an OpenAI account:
   - Click "Sign In" and enter your credentials
2. If you don't have an account:
   - Click "Sign Up"
   - Create an account using:
     - Email address, OR
     - Google account, OR
     - Microsoft account
   - Verify your email if required

### Step 3: Add Payment Method (Required)
⚠️ **Important:** OpenAI requires a payment method to use the API, even for free tier.

1. Go to: https://platform.openai.com/account/billing
2. Click "Add payment method"
3. Enter your credit/debit card details
4. **Note:** You get $5 free credit when you sign up, which is enough for testing!

### Step 4: Create Your API Key
1. Go to: https://platform.openai.com/api-keys
2. Click the **"+ Create new secret key"** button
3. Give it a name (optional, e.g., "Campus Compass")
4. Click **"Create secret key"**
5. **⚠️ IMPORTANT:** Copy the key immediately! It will only be shown once.
   - It looks like: `sk-proj-abc123xyz789...`
   - If you lose it, you'll need to create a new one

### Step 5: Add to Your .env File
1. Open the `.env` file in your project folder
2. Replace `your_key_here` with your actual key:
   ```
   OPENAI_API_KEY=sk-proj-your-actual-key-here
   ```
3. Save the file
4. **Never share this key or commit it to GitHub!**

---

## 💰 Pricing Information

- **Free Tier:** $5 free credit when you sign up
- **Pay-as-you-go:** Very affordable for testing
- **GPT-3.5-turbo:** ~$0.0015 per 1K tokens (very cheap!)
- For a typical question-answer session: ~$0.01-0.05

**Example:** With $5 free credit, you can ask hundreds of questions!

---

## 🔒 Security Tips

1. ✅ **DO:**
   - Keep your API key secret
   - Use it only in your `.env` file (which is in `.gitignore`)
   - Rotate keys if you suspect it's compromised

2. ❌ **DON'T:**
   - Share your API key publicly
   - Commit it to GitHub
   - Hardcode it in your Python files
   - Share screenshots with the key visible

---

## 🆘 Troubleshooting

### "Insufficient credits" error
- Add payment method at: https://platform.openai.com/account/billing
- Check your usage at: https://platform.openai.com/usage

### "Invalid API key" error
- Make sure you copied the entire key (starts with `sk-`)
- Check there are no extra spaces in your `.env` file
- Verify the key is active at: https://platform.openai.com/api-keys

### Can't see the API key after creation
- You need to create a new one (old keys are only shown once)
- Go to API keys page and create another key

---

## 📝 Quick Checklist

- [ ] Created OpenAI account
- [ ] Added payment method
- [ ] Created API key
- [ ] Copied the key (starts with `sk-`)
- [ ] Added to `.env` file as: `OPENAI_API_KEY=sk-your-key`
- [ ] Saved the `.env` file
- [ ] Ready to run the app!

---

## Alternative: Using Other LLMs

If you prefer not to use OpenAI, you can modify the code to use:
- **Hugging Face** (free, but slower)
- **Anthropic Claude** (requires API key)
- **Local models** (free, but requires powerful computer)

For now, OpenAI GPT-3.5-turbo is the easiest and most cost-effective option!

