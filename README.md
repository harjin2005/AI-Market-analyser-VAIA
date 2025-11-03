# VAIA Market Analyst
Autonomous market research Q&A and data extractor on any PDF/TXT — powered by LangGraph AI agents, HuggingFace embeddings, and ChromaDB.

<!-- Replace with a real screenshot or remove this line -->

## Features

⚡ **Ask Any Question about Your PDF**: Upload a market or financial report, get instant, grounded answers using agentic LLM RAG.  
🧩 **JSON Data Extraction**: Download structured market summaries (when present) — with "fail safe" output if data is missing.  
🧠 **Modern Agentic Routing**: Powered by LangGraph for tool calling/Q&A, with HuggingFace MiniLM embeddings for fast and cheap retrieval.  
🔒 **Prompt Injection & Security**: Multi-layer protection against malicious input and agent logic tampering (see our included case study!).  
🌎 **Docker Ready**: Spin up everywhere, reproducible outputs, .env-sample for easy local setup.

## Project File Importance Table

| File Name | Header Comment / Docstring | Purpose / Importance |
|----------------------------|----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| `README.md` | # VAIA Market Analyst – Autonomous market research Q&A and data extractor | Project overview, instructions, architecture, features, and usage—crucial for onboarding and documentation|
| `.env.example` | # Agentic AI Market Analyst - Environment Example | Example environment config—shows required keys and environment variables for setup |
| `requirements.txt` | *(No header comment – dependency list only)* | Specifies all Python package dependencies—required for environment setup |
| `main.py` | """Main script to setup and test the AI Market Analyst pipeline.""" | Step-by-step system setup and test harness for core pipeline |
| `config.py` | """Configuration settings for the AI Market Analyst using Groq and HuggingFace.""" | Centralizes config for LLM, embedding, vector DB, API—enables flexible, robust deployments |
| `document_processor.py` | """Document processing and chunking utilities.""" | Loads PDF/TXT files, chunks text for analysis—ensures reliable data ingestion |
| `vector_store.py` | """Vector store management with ChromaDB and HuggingFace embeddings.""" | Manages storage, retrieval, and querying of vectorized document data—boosts AI Q&A/Search |
| `agent.py` | """Agentic AI routing using LangGraph for autonomous tool selection.""" | Core autonomous LangGraph agent—intelligent tool routing/Q&A/Extraction |
| `tools.py` | """AI Agent tools using direct Groq API (no ChatGroq wrapper).""" | Implements the agent's core Q&A, summarization, and structured extraction tools |
| `api_main.py` | """FastAPI application for AI Market Analyst (Groq/HuggingFace).""" | Exposes the pipeline over REST—allows integration with UI/Streamlit or external systems |
| `streamlit_app.py` | *(No header, but imports all modules and sets up Streamlit UI)* | Handles interactive frontend—file upload, Q&A, summaries, data extraction in easy web interface |

## Visual Demo

Add a GIF or screenshot of your app here:
```
![Chat Screenshot](assets/demo.gif)
```

## Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/harjin2005/VAIA-Market-Analysis.git
cd VAIA-Market-Analysis
pip install -r requirements.txt
```

### 2. Configure API Keys
Copy the example env file:
```bash
cp .env-sample .env
```
Fill the `.env` with your Groq or OpenAI keys and model (see "Configuration" below).

### 3. Run Locally
```bash
streamlit run streamlit_app.py
```
Or with Docker:
```bash
docker build -t vaia-market-analyst .
docker run --env-file .env -p 8501:8501 vaia-market-analyst
```

## Usage

Navigate to the Streamlit app, upload a PDF/TXT file, and:

- **Chat**: Ask questions such as "What are the key market trends?" or "Extract the revenue figures."
- **JSON Extraction**: Click "Extract Market Data as JSON" for structured data output. If the PDF lacks data, you get an empty structure—no hallucinations.
- **View History**: Check stored vectorized chunks in your ChromaDB.

## Configuration

Key environment variables (`.env`):

```bash
GROQ_API_KEY=YOUR_GROQ_API_KEY
MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHROMA_PERSIST_DIR=./chroma_db
```

## Architecture

```
┌─────────────────────────────┐
│     User Interface          │
│   (Streamlit / FastAPI)     │
└───────────┬─────────────────┘
            │
            v
┌─────────────────────────────┐
│  LangGraph Agent (agent.py) │
│    (autonomous routing)     │
└───────────┬─────────────────┘
            │
      ┌─────┴─────┐
      │           │
      v           v
┌──────────┐  ┌─────────────┐
│  Tools   │  │ Vector DB   │
│(tools.py)│  │(vector_store│
│          │  │    .py)     │
└──────────┘  └─────────────┘
      │           │
      v           v
    ▼[Chat/JSON Output]
```

## Security

- All file uploads and user queries are chunked/sanitized.
- LLM only receives chunked context—never entire untrusted input.
- JSON extraction is schema-enforced.
- Prompt attacks fail safe, no hallucinated values.
- See `Case-Study_-Proactive-Defense-Against-Prompt-Injection-in-LLMs.pdf` for a full security rundown.

## FAQ

**Q: Why do some JSON fields return 0/empty?**  
A: If the PDF doesn't contain actual market values, the agent returns a blank/empty structure instead of inventing numbers—ensuring always-safe outputs.

**Q: How can I add more LLM tools?**  
A: Register a new tool with LangGraph and update your agent's tool list in your backend Python code.

## Contributing / License

PRs and feedback welcome! See LICENSE for open source terms.  
For support, open an issue or ping [@harjin2005](https://github.com/harjin2005).

- **Demo video**: (link here when ready)
- **Case study**: [Case Study: Proactive Defense Against Prompt Injection in LLMs](https://www.perplexity.ai/search/Case-Study_-Proactive-Defense-Against-Prompt-Injection-in-LLMs.pdf)

## Ready to try?

Clone, configure, and run — judge-ready in three commands.  
**Star⭐ if helpful!**
