# 🚀 How to Run Campus Compass - Step by Step

## Step 1: Create the .env File

1. In your project folder, create a new file named `.env` (just `.env`, no extension)
2. Open it in a text editor
3. Add this line (replace with your actual API key):
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```
4. Save the file

**To get your OpenAI API key:**
- Go to https://platform.openai.com/api-keys
- Sign in or create an account
- Click "Create new secret key"
- Copy the key and paste it in your `.env` file

---

## Step 2: Add Documents to Process

1. Open the `documents` folder in your project
2. Copy your college documents (PDF, DOCX, or TXT files) into this folder
3. Examples:
   - Student Handbook PDF
   - Academic Calendar
   - Library Rules
   - Fee Structure
   - Any official college document

**Quick Test:** You can copy the PDF files from your main folder (`Problem Statement HACK INFINITY.pdf`) to the `documents` folder just to test!

---

## Step 3: Run the Application

1. Open PowerShell or Command Prompt
2. Navigate to your project folder:
   ```powershell
   cd "C:\Users\vjain\Downloads\hack infinity"
   ```
3. Run this command:
   ```powershell
   streamlit run app.py
   ```
4. Your browser should automatically open to `http://localhost:8501`
   - If it doesn't, manually open your browser and go to that address

---

## Step 4: Process Your Documents

1. In the Streamlit app, look at the **sidebar on the left**
2. You'll see a section called "📚 Document Management"
3. Click the button **"🔄 Process Documents"**
4. Wait for it to finish (this may take 1-2 minutes)
5. You'll see a success message showing how many chunks were created

---

## Step 5: Ask Questions!

1. In the main area, you'll see a text box "Enter your question:"
2. Type your question, for example:
   - "What is this document about?"
   - "What are the main topics covered?"
   - "Summarize the key points"
3. Choose your question mode:
   - **Standard**: Regular questions
   - **Multi-Document**: Questions needing info from multiple sources
   - **Summarize**: Get bulleted summaries
4. Click **"🔍 Ask"**
5. Get your answer with source citations!

---

## Troubleshooting

### ❌ "API key not found" error
- Make sure `.env` file exists in the project root
- Check that the file has exactly: `OPENAI_API_KEY=your_key_here`
- No quotes around the key, no spaces

### ❌ "No documents found"
- Make sure files are in the `documents/` folder (not the main folder)
- Check file format is PDF, DOCX, or TXT

### ❌ App won't start
- Make sure you're in the correct directory
- Try: `python -m streamlit run app.py`

### ❌ Processing fails
- Check that documents aren't corrupted
- Try with a simple text file first to test

---

## Example Workflow

```
1. Create .env file → Add API key
2. Copy PDF to documents/ folder
3. Run: streamlit run app.py
4. Click "Process Documents" in sidebar
5. Wait for "✅ Successfully processed X chunks"
6. Type question: "What is this about?"
7. Click "Ask"
8. Read answer with sources!
```

---

## Need Help?

Check these files:
- `QUICKSTART.md` - Detailed guide
- `README.md` - Project overview
- `SETUP_INSTRUCTIONS.txt` - Quick reference

