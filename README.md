# VAIA Market Analyst

Autonomous market research Q&A and data extractor on any PDF/TXT — powered by LangGraph AI agents, HuggingFace embeddings, and ChromaDB.

<!-- Replace with a real screenshot or remove this line -->

## Features

⚡ **Ask Any Question about Your PDF**: Upload a market or financial report, get instant, grounded answers using agentic LLM RAG.

🧩 **JSON Data Extraction**: Download structured market summaries (when present) — with "fail safe" output if data is missing.

🧠 **Modern Agentic Routing**: Powered by LangGraph for tool calling/Q&A, with HuggingFace MiniLM embeddings for fast and cheap retrieval.

🔒 **Prompt Injection & Security**: Multi-layer protection against malicious input and agent logic tampering (see our included case study!).

🌎 **Docker Ready**: Spin up everywhere, reproducible outputs, .env-sample for easy local setup.

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

1. Upload your PDF or TXT report on the home screen.
2. Ask natural questions in the chat.
3. Download JSON summary (if relevant data is present in the document).
4. Clear chat and repeat for new research.

## Configuration

Edit `.env` with:

```
GROQ_API_KEY=your-groq-key
GROQ_MODEL=mixtral-8x7b-32768  # (or another supported model)
EMBEDDING_MODEL_TYPE=huggingface
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
VECTOR_DB_PATH=./chroma_db
COLLECTION_NAME=innovate_inc_docs
OPENAI_API_KEY=your-key  # (optional, if using OpenAI as fallback or for embedding)
```

## Architecture

```
User
 │
 ▼
[Streamlit UI] --Upload PDF--> [PDF/Text processor]
 │                                   │
 ▼                                   │
  ──► [Chunking & Embedding (MiniLM)]─┤
 │                                   ▼
 ▼                          [ChromaDB Vector Store]
[User Question]                     │
 │                                   ▼
 ▼                        [Retriever (semantic search)]
[LangGraph Agent: tool routing]     ▼
    │             ┌───────────────────┘
    ▼             |
[Q&A / JSON Extraction Tool] (LLM, tools, schema validation)
    │
    ▼
[Chat/JSON Output]
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
