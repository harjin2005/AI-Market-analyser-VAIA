# AI Market Analyser (VAIA)

An AI-powered, end-to-end market intelligence and analysis assistant that aggregates data from news, social media, and financial APIs to deliver actionable insights, risk signals, and investment research. Built for speed, clarity, and reliability with a modular architecture and production-ready tooling.

---

## Highlights
- Executive-ready reports with sentiment, trends, risks, and opportunities
- Multi-source ingestion: news, social, market data, and custom CSVs
- LLM-assisted synthesis with transparent sources and citations
- Reproducible pipelines, caching, and idempotent runs
- Secure secrets management and configurable runtime
- Beautiful outputs: dashboards, charts, and PDF/Markdown reports


## Demo
- Screenshots: add images under docs/images and reference below once available
  - Dashboard: docs/images/dashboard.png
  - Sentiment Heatmap: docs/images/sentiment-heatmap.png
  - Entity Trends: docs/images/entity-trends.png
- Loom/Video placeholder: docs/videos/vaia-demo.mp4 (optional)

```
![Dashboard](docs/images/dashboard.png)
![Sentiment Heatmap](docs/images/sentiment-heatmap.png)
![Entity Trends](docs/images/entity-trends.png)
```


## Architecture Overview
```
                +--------------------+
                |  Config & Secrets  |
                |  (.env, yaml)      |
                +----------+---------+
                           |
+----------+      +--------v-------+       +-------------------+
| Sources  |----->| Ingestion      |------>| Storage/Cache     |
| (News,   |      | (ETL connectors)|      | (SQLite/Parquet)  |
| Social,  |      +--------+-------+       +---------+---------+
| Market)  |               |                         |
+----------+               v                         v
                    +------+--------+        +-------+-------+
                    | NLP/LLM Core  |<------>| Feature Eng.  |
                    | (summaries,   |        | Signals, KPIs |
                    | sentiment, NER)|       +-------+-------+
                    +------+--------+                |
                           |                         v
                           v                 +-------+--------+
                    +------+--------+        | Visualization  |
                    | Report Builder|------->| (Plots/Dash)   |
                    | (MD/PDF/HTML) |        +----------------+
                    +---------------+
```


## Features
- Data ingestion from:
  - News APIs (NewsAPI, GDELT, etc.)
  - Social platforms (X/Twitter via API or exports)
  - Market data (Yahoo Finance, Alpha Vantage, Polygon.io)
  - Local files (CSV/JSON) for custom datasets
- Text analytics:
  - Sentiment analysis, topic modeling, entity recognition
  - LLM-based summarization with source grounding
- Signal generation:
  - Volatility alerts, momentum/trend flags, risk indicators
- Reporting:
  - Markdown and PDF export with charts and tables
  - Auto-generated executive summary and action items
- Observability & Ops:
  - Structured logging, retry + backoff, and request caching


## Tech Stack
- Python 3.10+
- FastAPI (optional API layer)
- LangChain / LiteLLM (LLM orchestration)
- OpenAI/Groq/Local models (configurable)
- Pandas, NumPy, scikit-learn
- SQLite/Parquet for local persistence
- Plotly/Matplotlib/Seaborn for visualization
- Typer for CLI, Pydantic for config


## Setup
1) Prerequisites
- Python 3.10+
- Make (optional), Git

2) Clone
- git clone https://github.com/harjin2005/AI-Market-analyser-VAIA.git
- cd AI-Market-analyser-VAIA

3) Environment
- cp .env.example .env
- Fill API keys: NEWSAPI_KEY, OPENAI_API_KEY, ALPHA_VANTAGE_KEY, etc.

4) Install
- python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
- pip install -U pip
- pip install -r requirements.txt

5) Verify
- python -m vaia.cli --help


## Usage
Common commands:
- Ingest latest news for a ticker/topic
  - python -m vaia.cli ingest --source newsapi --query "AAPL" --days 3
- Run full analysis pipeline
  - python -m vaia.cli analyze --query "AAPL" --outputs md,pdf
- Generate dashboard assets only
  - python -m vaia.cli visualize --input data/processed/latest.parquet
- Serve API (optional)
  - uvicorn vaia.api:app --reload

Outputs will be saved under outputs/ with time-stamped folders containing:
- report.md / report.pdf
- charts/*.png
- data/*.parquet


## Configuration
- Global config in config/config.yaml
- Secrets in .env (never commit this)
- Model/provider settings via env or YAML (e.g., OPENAI_API_KEY, LLM_PROVIDER)
- Toggle features (e.g., use_cache, enable_api, model_name)


## Security & Privacy
- Do not commit secrets: use .env and gitignore
- Minimal scope API keys; rotate regularly
- Optional local-only mode with offline models
- Respect robots.txt and terms of data providers
- PII-safe processing; redact sensitive terms in logs


## Development
- Lint & format: ruff, black
- Tests: pytest -q
- Pre-commit hooks: pre-commit install
- CI: GitHub Actions (tests + lint on PRs)


## Project Structure
```
vaia/
  api/                # FastAPI endpoints (optional)
  cli.py             # CLI entry points
  config/            # YAML configs
  core/              # LLM/NLP utilities
  etl/               # Ingestion connectors
  fe/                # Feature engineering
  reports/           # Templates/builders
  viz/               # Plot helpers
config/
  config.yaml
data/
  raw/ processed/
outputs/
  ...                # reports, charts, artifacts
```


## Roadmap
- [ ] Add social listening with streaming
- [ ] Plugin system for new data sources
- [ ] Vector search over knowledge base
- [ ] Fine-tuned summarization models
- [ ] Docker images and Helm chart


## Troubleshooting
- Install issues: ensure Python 3.10+ and pip >= 23
- API failures: check rate limits and keys in .env
- Empty outputs: increase date window or relax filters
- PDF errors: ensure wkhtmltopdf or use MD-only output


## Credits
- Built by Harjin and contributors
- Icons and illustrations: undraw.co (optional)
- Thanks to open-source libraries noted above

---

If this project helps you, give it a star and feel free to open issues or PRs!
