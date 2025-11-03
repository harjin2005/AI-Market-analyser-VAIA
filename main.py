"""Main script to setup and test the AI Market Analyst pipeline."""
from config import config
from document_processor import DocumentProcessor
from vector_store import VectorStoreManager
from agent import MarketAnalystAgent

def setup_system():
    print("="*70)
    print("AI MARKET ANALYST - SYSTEM SETUP")
    print("="*70)

    # Process document: chunking
    print("\n[1/4] Processing document...")
    processor = DocumentProcessor()
    chunks = processor.process_document(config.DOCUMENT_PATH)

    # Create vector store: embedding + storage
    print("\n[2/4] Creating vector store...")
    vector_store_manager = VectorStoreManager()
    vector_store = vector_store_manager.create_vector_store(chunks)

    # Initialize agent: autonomous routing
    print("\n[3/4] Initializing agent...")
    retriever = vector_store_manager.get_retriever(k=3)
    agent = MarketAnalystAgent(retriever)
    print("✓ Agent initialized with autonomous routing")

    print("\n[4/4] Testing basic pipeline...")
    test_queries = [
        "What is the market size for AI workflow automation?",
        "Summarize the competitive landscape",
        "Extract the structured data about market share"
    ]
    for q in test_queries:
        print(f"\n--- Query: {q}")
        print(agent.process_query(q))
        print("-" * 70)

    print("\n" + "="*70)
    print("✅ SYSTEM SETUP COMPLETE!")
    print("="*70)
    return agent, vector_store_manager

if __name__ == "__main__":
    setup_system()
