# Campus Compass - The AI Oracle for Your College

An AI-powered chatbot that serves as the single source of truth for all college-related queries using Retrieval-Augmented Generation (RAG).

## Features

- **Document Processing**: Ingests PDFs, DOCX, and TXT files
- **Vector Search**: Fast semantic search using ChromaDB
- **RAG Pipeline**: Accurate answers with source citations
- **Multi-Document Synthesis**: Answers questions requiring multiple sources
- **Policy Summarizer**: Concise summaries of college policies
- **Personalized Alerts**: Calendar-based reminders (coming soon)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your API key:
```
GOOGLE_API_KEY=your_google_api_key_here
```
Or use OpenAI:
```
OPENAI_API_KEY=your_openai_api_key_here
```

Get your Google API key from: https://aistudio.google.com/apikey

3. Place your college documents in the `documents/` folder (PDF, DOCX, or TXT format)

4. Run the application:
```bash
streamlit run app.py
```

## Usage

1. First, click "Process Documents" to index your documents
2. Ask any question about college policies, rules, or information
3. Get accurate answers with source citations

## Project Structure

```
.
├── app.py                 # Streamlit web interface
├── document_processor.py  # Document ingestion and processing
├── vector_store.py        # Vector database management
├── rag_pipeline.py        # RAG implementation
├── utils.py               # Utility functions
├── documents/             # Place your college documents here
└── vector_db/             # Vector database storage (auto-created)
```


