import streamlit as st
from config import config
from document_processor import DocumentProcessor
from vector_store import VectorStoreManager
from agent import MarketAnalystAgent
import json
import tempfile
import os

st.set_page_config(
    page_title="Agentic Market Analyst – VAIA Residency",
    page_icon="🤖",
    layout="wide"
)

def process_user_document(uploaded_file):
    # Save uploaded file safely
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        tmp.flush()
        doc_path = tmp.name

    # Process the document
    processor = DocumentProcessor()
    chunks = processor.process_document(doc_path)
    if not chunks or len(chunks) == 0:
        return None, None  # Signal to UI to show error and skip rest

    # Usual vector store and agent setup
    vector_store_manager = VectorStoreManager()
    vector_store_manager.create_vector_store(chunks)
    retriever = vector_store_manager.get_retriever(k=3)
    agent = MarketAnalystAgent(retriever)
    return agent, doc_path

@st.cache_resource
def default_pipeline():
    processor = DocumentProcessor()
    chunks = processor.process_document(config.DOCUMENT_PATH)
    vector_store_manager = VectorStoreManager()
    vector_store_manager.create_vector_store(chunks)
    retriever = vector_store_manager.get_retriever(k=3)
    agent = MarketAnalystAgent(retriever)
    return agent

# __ UPLOAD HANDLER IN SIDEBAR __
with st.sidebar:
    st.image("https://avatars.githubusercontent.com/harjin2005", width=80)
    st.markdown("## **Agentic AI Market Analyst - Harjinder singh**\n_VAIA Residency Project_")
    st.markdown("#### Features")
    st.markdown("""
- LangGraph-powered **autonomous** agent
- Upload your own text/PDF report!
- Market Q&A, summarization, & data extraction (JSON)
- Groq LLM backend, MiniLM, Chroma (open-source/free)
- Professional, demo-ready UI
    """)
    uploaded_file = st.file_uploader("Upload market research `.txt` or `.pdf`", type=["txt", "pdf"])
    if uploaded_file:
        agent_handle, doc_path = process_user_document(uploaded_file)
        if agent_handle is None:
            st.error("❌ Sorry, we couldn't extract usable text from that document. Try a different file (TXT or a PDF with selectable/copyable text).")
            st.stop()
        st.success(f"✅ Successfully uploaded and indexed '{uploaded_file.name}'!")
        st.session_state.agent = agent_handle
        st.session_state.cur_doc = doc_path
        st.session_state.chat_history = []
    else:
        if "agent" not in st.session_state:
            st.session_state.agent = default_pipeline()
            st.session_state.cur_doc = config.DOCUMENT_PATH

    st.caption("You can use the default Innovate Inc. doc, or upload your own.")

st.title("🤖 Agentic AI Market Analyst")
st.markdown("""
Analyze any business research doc (upload above or use default).  
Supports fully-autonomous routing: Q&A, summarization, and JSON data extraction.
""")
st.divider()

mode = st.radio(
    "Select Mode:",
    ["💬 Q&A Chat", "📝 Summarize", "📊 Extract Structured Data"],
    horizontal=True
)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

agent = st.session_state.agent

def parse_agent_response(text):
    # If the answer includes a <think>...</think> block, split it
    import re
    think_match = re.search(r"<think>(.*?)</think>", text, re.DOTALL | re.IGNORECASE)
    if think_match:
        think = think_match.group(1).strip()
        result = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE).strip()
        return think, result
    return None, text

if mode == "💬 Q&A Chat":
    st.markdown("#### Ask open-ended questions about your uploaded document or the default report.")

    # Display chat messages from history on app rerun
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask the agent your question..."):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Agent thinking..."):
                try:
                    raw_answer = agent.process_query(prompt)
                    print(f"[DEBUG] Full agent answer: {raw_answer}")
                    think, result = parse_agent_response(raw_answer)

                    if think:
                        st.info(f"🤔 Thinking...\n\n{think}")
                    
                    st.markdown(f"🤖 {result}")
                    answer_for_history = result

                except Exception as e:
                    answer_for_history = f"Error: {str(e)}"
                    print(f"[ERROR] {e}")
                    st.error(answer_for_history)
        
        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": answer_for_history})

    if st.button("Clear Chat History", key="clear_chat_qna"):
        st.session_state.chat_history.clear()
        st.success("Chat history cleared! Start new analysis.")
        st.rerun()

elif mode == "📝 Summarize":
    st.markdown("#### Summarize the research findings on a chosen aspect.")
    aspect = st.selectbox(
        "Choose an aspect to summarize:",
        ["overall", "competitors", "SWOT", "market_size", "recommendations"]
    )
    if st.button("Summarize Aspect", key="summarize_btn"):
        with st.spinner("Compiling market summary..."):
            try:
                summary = agent.agent_tools.summarize_tool(aspect)
                think, result = parse_agent_response(summary)
                if think:
                    st.info(f"🤔 Thinking...\n\n{think}")
                st.success("Summary ready!")
                st.markdown("🤖 " + result)
            except Exception as e:
                st.error(f"Error: {e}")

elif mode == "📊 Extract Structured Data":
    st.markdown("#### Extract market data as structured JSON.")
    if st.button("Extract JSON Data", key="extract_btn"):
        with st.spinner("Extracting..."):
            try:
                data = agent.agent_tools.extract_data_tool()
                st.markdown("Market data extracted below. Download as needed!")
                st.json(data)
                st.download_button(
                    label="Download as JSON",
                    data=json.dumps(data, indent=2),
                    file_name="market_data.json",
                    mime="application/json",
                    key="download_json_btn"
                )
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()
st.markdown("""
<sub>
Built for VAIA Agentic AI Residency: supports .txt/.pdf upload, chunking, MiniLM/Chroma embeddings, fully autonomous LLM routing, COT/think separation, and real Q&A.<br>
Contact: [your name]
</sub>
""", unsafe_allow_html=True)