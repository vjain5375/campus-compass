# AI Study Assistant - Multi-Agent System

A personalized study assistant powered by multiple AI agents that helps students learn more effectively through automated flashcard generation, adaptive quizzes, smart revision planning, and contextual question answering.

## 🎯 Features

### Core Agents

1. **Reader Agent** 📖
   - Extracts text from PDFs, DOCX, and TXT files
   - Classifies content into topics and subtopics
   - Segments material into manageable chunks
   - Supports both text and image-based documents

2. **Flashcard Agent** 📇
   - Automatically generates Q/A flashcards from study materials
   - Creates concise, effective learning cards
   - Supports topic-specific flashcard generation
   - Saves flashcards for offline review

3. **Quiz Agent** 📝
   - Generates multiple-choice questions with adaptive difficulty
   - Supports Easy, Medium, and Hard difficulty levels
   - Adapts quiz difficulty based on user performance
   - Provides detailed explanations for each question

4. **Planner Agent** 📅
   - Creates smart revision schedules
   - Distributes topics across study days
   - Tracks progress and completion
   - Provides reminders for upcoming revisions

5. **Chat/Doubt Agent** 💬
   - Answers contextual questions from uploaded materials
   - Uses RAG (Retrieval-Augmented Generation) for accurate answers
   - Provides source citations
   - Explains concepts with examples

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Agent Controller                │
│  (Orchestrates all agents)              │
└─────────────────────────────────────────┘
           │
           ├─── Reader Agent ───> Extract & Structure
           ├─── Flashcard Agent ───> Generate Q/A Cards
           ├─── Quiz Agent ───> Create Adaptive Quizzes
           ├─── Planner Agent ───> Build Revision Schedule
           └─── Chat Agent ───> Answer Questions
                    │
                    ▼
         ┌──────────────────────┐
         │  Knowledge Memory    │
         │  (Shared Context)    │
         └──────────────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │   Vector Store       │
         │   (ChromaDB)         │
         └──────────────────────┘
```

## 🚀 Installation

1. **Clone or download the repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key:**
   - Create a `.env` file in the project root
   - Add your Google API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```
   - Or use OpenAI:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 📖 Usage Guide

### Step 1: Upload Study Materials
- Click "Upload Study Materials" in the sidebar
- Select PDF, DOCX, or TXT files
- Click "Save Documents"
- Click "Process Documents" to extract and index content

### Step 2: Generate Flashcards
- Navigate to "Flashcards" page
- Select number of flashcards (5-30)
- Click "Generate Flashcards"
- Review and study the generated Q/A pairs

### Step 3: Take Quizzes
- Go to "Quizzes" page
- Select difficulty level (Easy/Medium/Hard)
- Choose number of questions
- Enable "Adaptive" mode for personalized difficulty
- Answer questions and submit to see results

### Step 4: Create Revision Plan
- Visit "Revision Planner" page
- Set your exam date
- Choose study days per week
- Click "Create Revision Plan"
- Track your progress and mark completed items

### Step 5: Ask Questions
- Use "Chat Assistant" to ask questions
- Get answers based on your uploaded materials
- View source citations for each answer

### Step 6: View Analytics
- Check "Analytics" page for progress tracking
- View study statistics and performance metrics
- Monitor revision completion rates

## 📁 Project Structure

```
study-assistant/
├── agents/
│   ├── __init__.py
│   ├── reader_agent.py      # Document reading and topic classification
│   ├── flashcard_agent.py    # Flashcard generation
│   ├── quiz_agent.py         # Quiz generation and evaluation
│   ├── planner_agent.py      # Revision planning
│   ├── chat_agent.py         # Question answering
│   └── controller.py         # Central orchestration
├── outputs/
│   ├── flashcards.json       # Generated flashcards
│   ├── quizzes.json          # Generated quizzes
│   └── planner.json          # Revision plans
├── documents/                # Upload study materials here
├── vector_db/                # Vector database (auto-created)
├── app.py                    # Main Streamlit application
├── vector_store.py           # Vector database management
├── utils.py                  # Utility functions
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🔧 Technical Stack

- **Frontend:** Streamlit
- **Backend:** Python (FastAPI-ready architecture)
- **LLM:** Google Gemini 2.0 Flash (or OpenAI)
- **Vector DB:** ChromaDB
- **Embeddings:** Sentence Transformers (all-MiniLM-L6-v2)
- **Document Processing:** PyPDF2, python-docx

## 🎓 Workflow

1. **Upload** → PDF/DOCX/TXT files
2. **Extract** → Reader Agent processes documents
3. **Chunk** → Text segmented into topics
4. **Embed** → Create vector embeddings
5. **Generate** → Flashcards, Quizzes, Planner
6. **Chat** → Ask questions and get answers
7. **Track** → Monitor progress and performance

## 📊 Features in Detail

### Adaptive Learning
- Quiz difficulty adjusts based on performance
- Revision plan prioritizes difficult topics
- Weak areas are automatically identified

### Smart Chunking
- Text segmented by topics, not just size
- Context preserved across chunks
- Topic classification using LLM

### Progress Tracking
- Completion rates for revision plans
- Quiz performance history
- Study streak tracking (coming soon)

## 🛠️ Customization

### Adjust Chunk Size
Edit `agents/reader_agent.py`:
```python
ReaderAgent(chunk_size=1500, chunk_overlap=300)
```

### Change LLM Model
Edit agent files to use different models:
```python
ChatGoogleGenerativeAI(model="gemini-pro")
```

### Modify Difficulty Levels
Edit `agents/quiz_agent.py` to customize difficulty criteria.

## 📝 Notes

- First-time document processing may take a few minutes
- Vector embeddings are cached for faster subsequent searches
- All generated content is saved in `outputs/` directory
- Documents are stored in `documents/` directory

## 🤝 Contributing

This is a hackathon project. Feel free to extend and improve!

## 📄 License

Open source - feel free to use and modify.

## 🙏 Acknowledgments

- Built with LangChain and Streamlit
- Powered by Google Gemini AI
- Vector search with ChromaDB

---

**Happy Studying! 📚✨**

