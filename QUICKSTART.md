# 🚀 Quick Start Guide

## Step 1: Set Up Your OpenAI API Key

1. Get your API key from: https://platform.openai.com/api-keys
2. Create a file named `.env` in the project root
3. Add this line to the `.env` file:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

## Step 2: Add Your College Documents

1. Place your college documents (PDF, DOCX, or TXT) in the `documents/` folder
2. Examples of documents you can add:
   - Student Handbook
   - Academic Calendar
   - Library Rules
   - Fee Structure
   - Hostel Regulations
   - Course Catalog

## Step 3: Run the Application

Open your terminal in this directory and run:
```bash
streamlit run app.py
```

The app will open in your browser automatically!

## Step 4: Process Documents

1. In the app sidebar, click **"🔄 Process Documents"**
2. Wait for the processing to complete (this may take a few minutes)
3. You'll see a success message with the number of chunks created

## Step 5: Ask Questions!

1. Type your question in the input box
2. Choose your question mode:
   - **Standard**: Regular questions
   - **Multi-Document**: Questions requiring info from multiple sources
   - **Summarize**: Get bulleted summaries of policies
3. Click **"🔍 Ask"** and get your answer with source citations!

## Example Questions

- "What's the fine for a late library book?"
- "When is the last day to drop a course?"
- "What are the hostel rules?"
- "Summarize the plagiarism policy"
- "What's the fee structure for international students?"

## Troubleshooting

- **API Key Error**: Make sure your `.env` file exists and has the correct API key
- **No Documents Found**: Check that files are in the `documents/` folder
- **Processing Fails**: Make sure documents are not corrupted and are in supported formats (PDF, DOCX, TXT)

