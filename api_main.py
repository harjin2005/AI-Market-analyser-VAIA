"""FastAPI application for AI Market Analyst (Groq/HuggingFace)."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from config import config
from document_processor import DocumentProcessor
from vector_store import VectorStoreManager
from agent import MarketAnalystAgent

app = FastAPI(
    title="AI Market Analyst API",
    description="Agentic AI system for market research document analysis",
    version="1.0.0"
)

agent = None
vector_store_manager = None

class QueryRequest(BaseModel):
    query: str
    mode: Optional[str] = "auto"  # auto, qa, summarize, extract

class QueryResponse(BaseModel):
    query: str
    response: str
    mode: str

class ExtractionResponse(BaseModel):
    data: Dict[str, Any]

@app.on_event("startup")
async def startup_event():
    global agent, vector_store_manager
    print("Initializing AI Market Analyst pipeline...")
    processor = DocumentProcessor()
    chunks = processor.process_document(config.DOCUMENT_PATH)
    vector_store_manager = VectorStoreManager()
    vector_store_manager.create_vector_store(chunks)
    retriever = vector_store_manager.get_retriever(k=3)
    agent = MarketAnalystAgent(retriever)
    print("✓ System initialized successfully!")

@app.get("/")
async def root():
    return {
        "message": "AI Market Analyst API",
        "status": "running",
        "endpoints": {
            "query": "/api/query",
            "qa": "/api/qa",
            "summarize": "/api/summarize",
            "extract": "/api/extract",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agent_initialized": agent is not None,
        "vector_store_initialized": vector_store_manager is not None
    }

@app.post("/api/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    try:
        response = agent.process_query(request.query)
        return QueryResponse(
            query=request.query,
            response=response,
            mode="auto"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/qa", response_model=QueryResponse)
async def qa_endpoint(request: QueryRequest):
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    try:
        response = agent.agent_tools.qa_tool(request.query)
        return QueryResponse(
            query=request.query,
            response=response,
            mode="qa"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/summarize", response_model=QueryResponse)
async def summarize_endpoint(request: QueryRequest):
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    try:
        aspect = request.query if request.query else "overall"
        response = agent.agent_tools.summarize_tool(aspect)
        return QueryResponse(
            query=request.query,
            response=response,
            mode="summarize"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/extract", response_model=ExtractionResponse)
async def extract_endpoint():
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    try:
        data = agent.agent_tools.extract_data_tool("all")
        return ExtractionResponse(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)
