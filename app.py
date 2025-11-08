"""
Campus Compass - Main Streamlit Application
The AI Oracle for Your College
"""

import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
from document_processor import DocumentProcessor
from vector_store import VectorStore
from rag_pipeline import RAGPipeline
from alerts_manager import AlertsManager
from utils import ensure_documents_directory, get_document_files, format_sources, get_latest_document, detect_multi_document_intent

# Load .env file at the start - try multiple methods
def load_api_key():
    """Load API key from .env file or Streamlit secrets (supports Google API key)"""
    api_key = None
    
    # Method 1: Try Streamlit secrets first (for Streamlit Cloud)
    try:
        if hasattr(st, 'secrets') and st.secrets:
            api_key = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("OPENAI_API_KEY")
            if api_key:
                os.environ['GOOGLE_API_KEY'] = api_key
                return api_key
    except Exception:
        pass
    
    # Method 2: Try environment variables (already set)
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key
    
    # Method 3: Try .env file (for local development)
    possible_paths = [
        Path(__file__).parent / '.env',  # Same directory as app.py
        Path('.env'),  # Current working directory
        Path.cwd() / '.env',  # Explicit current directory
    ]
    
    # Try load_dotenv
    for env_path in possible_paths:
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=True)
            # Try Google API key first, then OpenAI for backward compatibility
            api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("OPENAI_API_KEY")
            if api_key:
                break
    
    # Method 4: Read directly from file (most reliable fallback)
    if not api_key:
        for env_path in possible_paths:
            if env_path.exists():
                try:
                    with open(env_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            line_clean = line.strip()
                            # Check for Google API key first, then OpenAI
                            if line_clean and '=' in line_clean:
                                if 'GOOGLE_API_KEY' in line_clean:
                                    api_key = line_clean.split('=', 1)[1].strip()
                                    api_key = api_key.strip('"').strip("'")
                                    os.environ['GOOGLE_API_KEY'] = api_key
                                    break
                                elif 'OPENAI_API_KEY' in line_clean:
                                    api_key = line_clean.split('=', 1)[1].strip()
                                    api_key = api_key.strip('"').strip("'")
                                    os.environ['OPENAI_API_KEY'] = api_key
                                    break
                        if api_key:
                            break
                except Exception:
                    continue
    
    return api_key

# Page configuration (must be first Streamlit command)
st.set_page_config(
    page_title="Campus Compass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Campus Compass - AI-powered college Q&A system"
    }
)

# Custom CSS for attractive UI
st.markdown("""
<style>
    /* Main styling */
    .main {
        padding-top: 2rem;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        text-align: center;
    }
    
    .header-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        font-size: 1.5rem;
        color: rgba(255,255,255,0.95);
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    .header-description {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.9);
        margin-top: 1rem;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        transition: transform 0.2s;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Input styling */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    
    /* Answer container */
    .answer-container {
        background: linear-gradient(135deg, #f6f8fb 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .badge-primary {
        background: #667eea;
        color: white;
    }
    
    .badge-success {
        background: #10b981;
        color: white;
    }
    
    .badge-warning {
        background: #f59e0b;
        color: white;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Chat message styling */
    .chat-question {
        background: #667eea;
        color: white;
        padding: 1rem;
        border-radius: 15px 15px 5px 15px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .chat-answer {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 5px 15px 15px 15px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Load API key after Streamlit is initialized (so secrets are available)
load_api_key()

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = None
if 'documents_processed' not in st.session_state:
    st.session_state.documents_processed = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'alerts_manager' not in st.session_state:
    st.session_state.alerts_manager = AlertsManager()
if 'alerts_enabled' not in st.session_state:
    st.session_state.alerts_enabled = True
if 'session_initialized' not in st.session_state:
    st.session_state.session_initialized = False


def clear_all_data():
    """Clear all data: vector store, chat history, documents, and reset flags"""
    # Delete all document files from documents folder
    try:
        existing_docs = get_document_files()
        for doc_path in existing_docs:
            try:
                Path(doc_path).unlink()
            except Exception:
                pass  # Ignore errors when deleting files
    except Exception:
        pass
    
    # Clear vector store collection (even if not in session state, clear from disk)
    try:
        # Try to clear existing vector store if it exists
        if st.session_state.vector_store is not None:
            st.session_state.vector_store.clear_collection()
        else:
            # If vector store not initialized, create a temporary one to clear the collection
            temp_vector_store = VectorStore()
            temp_vector_store.clear_collection()
    except Exception:
        # If clearing fails, that's okay - will be cleared on next initialization
        pass
    
    # Reset vector store and RAG pipeline
    st.session_state.vector_store = None
    st.session_state.rag_pipeline = None
    
    # Clear chat history
    st.session_state.chat_history = []
    
    # Reset processing status
    st.session_state.documents_processed = False
    
    # Clear alerts deadlines
    try:
        st.session_state.alerts_manager.clear_deadlines()
    except Exception:
        pass


def initialize_components():
    """Initialize vector store and RAG pipeline"""
    # Reload API key to ensure it's available
    api_key = load_api_key()
    
    if st.session_state.vector_store is None:
        with st.spinner("Initializing vector store..."):
            st.session_state.vector_store = VectorStore()
    if st.session_state.rag_pipeline is None:
        with st.spinner("Initializing RAG pipeline..."):
            # Check API key before initializing
            if not api_key:
                st.error("⚠️ API key not found! Please check your .env file.")
                st.info("Make sure the .env file is in the same folder as app.py")
                st.info("Add either: GOOGLE_API_KEY=your_key or OPENAI_API_KEY=your_key")
                st.stop()
            st.session_state.rag_pipeline = RAGPipeline(st.session_state.vector_store)


def process_documents():
    """Process all documents in the documents directory"""
    docs_dir = ensure_documents_directory()
    doc_files = get_document_files()
    
    if not doc_files:
        st.error("No documents found in the 'documents' folder. Please add PDF, DOCX, or TXT files.")
        return False
    
    # Show which documents will be processed
    doc_names = [Path(doc).name for doc in doc_files]
    
    with st.spinner(f"Processing {len(doc_files)} document(s): {', '.join(doc_names)}..."):
        processor = DocumentProcessor()
        all_chunks = processor.process_directory(str(docs_dir))
        
        if not all_chunks:
            st.error("No text could be extracted from the documents.")
            return False
        
        # Count chunks per document for verification
        chunks_by_source = {}
        for chunk in all_chunks:
            source = chunk.get('metadata', {}).get('source', 'Unknown')
            chunks_by_source[source] = chunks_by_source.get(source, 0) + 1
        
        # Clear existing data and add new chunks
        st.session_state.vector_store.clear_collection()
        st.session_state.vector_store.add_documents(all_chunks)
        
        # Extract deadlines from documents for alerts
        try:
            st.session_state.alerts_manager.add_deadlines_from_documents(all_chunks)
        except Exception as e:
            st.warning(f"Could not extract deadlines: {e}")
        
        st.session_state.documents_processed = True
        
        # Show detailed success message
        success_msg = f"✅ Successfully processed {len(all_chunks)} chunks from {len(doc_files)} document(s)!\n\n"
        success_msg += "**Documents processed:**\n"
        for source, count in chunks_by_source.items():
            success_msg += f"  • {source}: {count} chunks\n"
        
        st.success(success_msg)
        return True


def main():
    """Main application"""
    # Clear all data on page refresh (new session) - ALWAYS clear on new session
    # This ensures a fresh start every time the page is refreshed
    if 'session_initialized' not in st.session_state or not st.session_state.get('session_initialized', False):
        # Clear everything: documents, vector store, chat history
        clear_all_data()
        st.session_state.session_initialized = True
    
    # Attractive Header with Gradient
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🧭 Campus Compass</h1>
        <p class="header-subtitle">The AI Oracle for Your College</p>
        <p class="header-description">✨ Ask anything about college policies, rules, and information. Get instant, accurate answers with source citations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin: 0;">⚡ Instant Answers</h3>
            <p style="margin: 0.5rem 0 0 0; color: #666;">Get answers in seconds</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin: 0;">📚 Multi-Document</h3>
            <p style="margin: 0.5rem 0 0 0; color: #666;">Synthesize from all sources</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin: 0;">🔔 Smart Alerts</h3>
            <p style="margin: 0.5rem 0 0 0; color: #666;">Never miss deadlines</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin: 0;">🎯 Accurate</h3>
            <p style="margin: 0.5rem 0 0 0; color: #666;">Cited sources included</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        # Check for API key (silently, only show error if missing)
        api_key = load_api_key() or os.getenv("GOOGLE_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("⚠️ API key not found! Please configure your API key in the .env file.")
            st.stop()
        
        # Document processing section with attractive header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <h2 style="color: white; margin: 0; text-align: center;">📚 Document Management</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # File uploader for new documents with attractive styling
        st.markdown("### 📤 Upload Documents")
        st.markdown("""
        <div style="background: #f0f4ff; padding: 1rem; border-radius: 10px; border: 2px dashed #667eea; margin: 1rem 0;">
            <p style="margin: 0; color: #667eea; text-align: center; font-weight: 500;">
                📎 Drag and drop files here or click to browse
            </p>
        </div>
        """, unsafe_allow_html=True)
        uploaded_files = st.file_uploader(
            "Upload college documents (PDF, DOCX, or TXT)",
            type=['pdf', 'docx', 'doc', 'txt'],
            accept_multiple_files=True,
            help="Upload one or more documents. They will be added to your existing documents.",
            label_visibility="collapsed"
        )
        
        if uploaded_files:
            if st.button("💾 Save Uploaded Documents", type="primary", use_container_width=True):
                docs_dir = ensure_documents_directory()
                
                with st.spinner("Saving documents..."):
                    saved_count = 0
                    skipped_count = 0
                    errors = []
                    
                    try:
                        for uploaded_file in uploaded_files:
                            try:
                                # Determine file extension
                                file_ext = Path(uploaded_file.name).suffix.lower()
                                if file_ext not in ['.pdf', '.docx', '.doc', '.txt']:
                                    errors.append(f"{uploaded_file.name}: Unsupported format")
                                    skipped_count += 1
                                    continue
                                
                                # Get target file path
                                file_path = docs_dir / uploaded_file.name
                                
                                # If file with same name exists, skip it (don't overwrite)
                                if file_path.exists():
                                    skipped_count += 1
                                    errors.append(f"{uploaded_file.name}: File already exists (skipped)")
                                    continue
                                
                                # Save new file
                                with open(file_path, "wb") as f:
                                    f.write(uploaded_file.getbuffer())
                                saved_count += 1
                                
                            except Exception as e:
                                errors.append(f"{uploaded_file.name}: {str(e)}")
                                skipped_count += 1
                        
                        # Show results
                        if saved_count > 0:
                            st.success(f"✅ Saved {saved_count} document(s)!")
                        if skipped_count > 0:
                            for error in errors:
                                st.warning(f"⚠️ {error}")
                        
                        if saved_count > 0:
                            st.info("Click 'Process Documents' below to index the new documents.")
                            # Don't clear vector store - just mark that reprocessing is needed
                            st.session_state.documents_processed = False
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error saving documents: {str(e)}")
        
        st.divider()
        
        # Show existing documents with attractive styling
        st.markdown("### 📁 Existing Documents")
        doc_files = get_document_files()
        if doc_files:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 0.75rem; border-radius: 10px; margin: 1rem 0; text-align: center;">
                <p style="color: white; margin: 0; font-weight: 600;">📚 Found {len(doc_files)} document(s)</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("📁 No documents found. Upload documents to get started!")
        
        if doc_files:
            with st.expander("📋 View Documents", expanded=False):
                for idx, doc in enumerate(doc_files):
                    doc_path = Path(doc)
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #667eea;">
                        <p style="margin: 0; font-weight: 500; color: #333;">📄 {doc_path.name}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    # Use full path hash or index to ensure unique key
                    unique_key = f"delete_{hash(str(doc_path))}_{idx}"
                    if st.button("🗑️ Delete", key=unique_key, help=f"Delete {doc_path.name}", use_container_width=True):
                        try:
                            doc_path.unlink()
                            st.success(f"✅ Deleted {doc_path.name}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting: {e}")
        
        st.divider()
        
        # Process documents button with attractive styling
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Process Documents", type="primary", use_container_width=True):
            initialize_components()
            if process_documents():
                st.session_state.chat_history = []  # Clear chat history
                st.balloons()  # Celebration effect!
        
        # Show vector store status with attractive styling
        if st.session_state.vector_store:
            count = st.session_state.vector_store.get_collection_count()
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; text-align: center; margin: 1rem 0;">
                <h3 style="color: white; margin: 0; font-size: 2rem;">{count}</h3>
                <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;">Indexed Chunks</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Personalized Alerts Section with attractive header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <h2 style="color: white; margin: 0; text-align: center;">🔔 Personalized Alerts</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Opt-in toggle
        alerts_enabled = st.checkbox(
            "Enable Alerts & Reminders",
            value=st.session_state.alerts_enabled,
            help="Get reminders for deadlines, fee payments, and important dates"
        )
        st.session_state.alerts_enabled = alerts_enabled
        st.session_state.alerts_manager.opt_in_user("default", alerts_enabled)
        
        # Show upcoming alerts
        if alerts_enabled:
            upcoming = st.session_state.alerts_manager.get_upcoming_deadlines(days_ahead=30)
            if upcoming:
                st.info(f"📅 {len(upcoming)} upcoming deadline(s) in the next 30 days")
                with st.expander("View Upcoming Deadlines"):
                    for alert in upcoming[:10]:  # Show top 10
                        days = alert.get('days_until', 0)
                        date_str = alert.get('date', '')
                        event = alert.get('event', 'Deadline')
                        source = alert.get('source', 'Unknown')
                        
                        # Format date
                        try:
                            from datetime import datetime as dt
                            date_obj = dt.fromisoformat(date_str)
                            date_formatted = date_obj.strftime("%B %d, %Y")
                        except:
                            date_formatted = date_str
                        
                        # Color code by urgency
                        if days <= 7:
                            st.warning(f"⚠️ **{date_formatted}** ({days} days) - {event}")
                        elif days <= 14:
                            st.info(f"📌 **{date_formatted}** ({days} days) - {event}")
                        else:
                            st.text(f"📅 **{date_formatted}** ({days} days) - {event}")
                        
                        st.caption(f"Source: {source}")
                        st.divider()
            else:
                st.info("No upcoming deadlines found. Process documents with calendar information to see alerts.")
        else:
            st.caption("Alerts are disabled. Enable above to see reminders.")
        
        st.divider()
        
        # Clear data button
        if st.button("🗑️ Clear All Data", use_container_width=True):
            # Delete all document files
            try:
                existing_docs = get_document_files()
                for doc_path_str in existing_docs:
                    doc_path_obj = Path(doc_path_str)
                    try:
                        if doc_path_obj.exists():
                            doc_path_obj.unlink()
                    except Exception:
                        pass
            except Exception:
                pass
            
            # Clear vector store and other data
            if st.session_state.vector_store:
                st.session_state.vector_store.clear_collection()
            st.session_state.documents_processed = False
            st.session_state.chat_history = []
            st.session_state.alerts_manager.clear_deadlines()
            st.success("All data and documents cleared!")
            st.rerun()
        
        st.divider()
        
        # Instructions
        with st.expander("📖 How to Use"):
            st.markdown("""
            **For New Users:**
            1. **Upload Documents**: Use the file uploader above to add one or more college documents
            2. **Save Documents**: Click "Save Uploaded Documents" to add them (existing documents are preserved)
            3. **Process**: Click "Process Documents" to index all documents
            4. **Ask Questions**: Type your question in the chat below
            5. **Get Answers**: Receive accurate answers with source citations
            
            **Note**: 
            - You can upload multiple documents at once
            - New documents are added to existing ones (not replaced)
            - Documents are only cleared on page refresh or when clicking "Clear All Data"
            - If a file with the same name already exists, it will be skipped
            
            **Alternative**: You can also manually place PDF, DOCX, or TXT files in the `documents/` folder
            
            **Bonus Features**:
            - Use "Multi-Document" mode for complex questions
            - Use "Summarize" for policy summaries
            - **Enable Alerts** to get reminders for deadlines and important dates
            - Delete individual documents using the 🗑️ button
            """)
    
    # Initialize components
    initialize_components()
    
    # Check if documents are processed - with attractive welcome message
    if not st.session_state.documents_processed:
        if st.session_state.vector_store:
            count = st.session_state.vector_store.get_collection_count()
            if count > 0:
                st.session_state.documents_processed = True
            else:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%); padding: 2rem; border-radius: 15px; text-align: center; margin: 2rem 0;">
                    <h2 style="color: #2d3436; margin: 0;">🚀 Get Started!</h2>
                    <p style="color: #636e72; margin: 1rem 0 0 0; font-size: 1.1rem;">
                        👆 Upload and process documents using the sidebar to start asking questions!
                    </p>
                    <p style="color: #636e72; margin: 0.5rem 0 0 0;">
                        📤 Upload → 💾 Save → 🔄 Process → 💬 Ask Questions
                    </p>
                </div>
                """, unsafe_allow_html=True)
                return
    
    # Show alerts banner if enabled and there are urgent deadlines
    if st.session_state.alerts_enabled:
        upcoming = st.session_state.alerts_manager.get_upcoming_deadlines(days_ahead=7)
        urgent = [a for a in upcoming if a.get('days_until', 999) <= 7]
        if urgent:
            st.warning(f"🔔 **Urgent Alert:** {len(urgent)} deadline(s) in the next 7 days! Check the sidebar for details.")
    
    # Main chat interface with attractive styling
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; margin: 2rem 0;">
        <h2 style="color: white; margin: 0; text-align: center;">💬 Ask Your Question</h2>
        <p style="color: rgba(255,255,255,0.9); text-align: center; margin: 0.5rem 0 0 0;">Get instant answers from your college documents</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Question type selector with better styling
    st.markdown("### 🎯 Question Mode")
    col1, col2, col3 = st.columns(3)
    with col1:
        question_mode = st.radio(
            "Mode",
            ["Standard", "Multi-Document", "Summarize"],
            horizontal=True,
            help="Standard: Single answer (prioritizes latest document)\nMulti-Document: Synthesize from multiple sources\nSummarize: Bulleted summary",
            label_visibility="collapsed"
        )
    
    # Chat history display with attractive styling
    if st.session_state.chat_history:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📜 Chat History")
        for i, (question, answer, sources) in enumerate(st.session_state.chat_history):
            st.markdown(f"""
            <div class="chat-question">
                <strong>Q{i+1}:</strong> {question}
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="chat-answer">
                <strong>Answer:</strong><br>{answer}
            </div>
            """, unsafe_allow_html=True)
            if sources:
                source_badges = " ".join([f'<span class="badge badge-success">{s}</span>' for s in sources])
                st.markdown(f'<div style="margin: 0.5rem 0;">📎 {source_badges}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
    
    # Question input with attractive styling
    st.markdown("<br>", unsafe_allow_html=True)
    question = st.text_input(
        "💭 Enter your question:",
        placeholder="e.g., What's the fine for a late library book? Or ask about policies, deadlines, fees...",
        key="question_input",
        label_visibility="visible"
    )
    
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        ask_button = st.button("🔍 Ask", type="primary", use_container_width=True)
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # Process question
    if ask_button and question:
        if not st.session_state.rag_pipeline:
            st.error("RAG pipeline not initialized. Please process documents first.")
            return
        
        with st.spinner("Searching documents and generating answer..."):
            # Auto-detect multi-document intent from question
            auto_multi_doc = detect_multi_document_intent(question)
            
            # Select appropriate method based on mode or auto-detection
            if question_mode == "Multi-Document" or auto_multi_doc:
                # Use multi-document mode if explicitly selected or auto-detected
                if auto_multi_doc and question_mode != "Multi-Document":
                    st.info("💡 Detected multi-document intent - using multi-document synthesis")
                result = st.session_state.rag_pipeline.answer_multi_document_question(question, n_chunks=12, allow_general=True)
            elif question_mode == "Summarize":
                result = st.session_state.rag_pipeline.answer_question(question, n_chunks=10, summarize=True, allow_general=True)
            else:
                # Standard mode: prioritize latest uploaded document
                latest_doc = get_latest_document()
                result = st.session_state.rag_pipeline.answer_question(
                    question, 
                    n_chunks=10, 
                    allow_general=True,
                    prioritize_source=latest_doc
                )
            
            # Display answer in attractive container
            st.markdown("""
            <div class="answer-container">
                <h2 style="color: #667eea; margin-top: 0;">💡 Answer</h2>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(result['answer'])
            
            # Display sources with badges
            if result['sources']:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 📎 Sources")
                source_badges = " ".join([f'<span class="badge badge-primary">{source}</span>' for source in result['sources']])
                st.markdown(f'<div style="margin: 1rem 0;">{source_badges}</div>', unsafe_allow_html=True)
            
            # Add to chat history
            st.session_state.chat_history.append((
                question,
                result['answer'],
                result['sources']
            ))
            
            # Show retrieved chunks (expandable)
            with st.expander("🔍 View Retrieved Context"):
                for i, chunk in enumerate(result['chunks'][:3], 1):  # Show top 3
                    st.markdown(f"**Chunk {i}** (from {chunk['metadata'].get('source', 'Unknown')}):")
                    st.text(chunk['text'][:300] + "..." if len(chunk['text']) > 300 else chunk['text'])
                    st.caption(f"Distance: {chunk.get('distance', 'N/A'):.4f}" if chunk.get('distance') else "")
    
    # Attractive Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 2rem; border-radius: 15px; text-align: center; margin-top: 3rem;">
        <p style="color: #667eea; font-weight: 600; margin: 0; font-size: 1.1rem;">
            🧭 Campus Compass
        </p>
        <p style="color: #666; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            Built with RAG (Retrieval-Augmented Generation) | Powered by Google Gemini & ChromaDB
        </p>
        <p style="color: #999; margin: 0.5rem 0 0 0; font-size: 0.8rem;">
            ✨ Your AI-powered college information assistant
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

