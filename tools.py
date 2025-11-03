"""AI Agent tools using direct Groq API (no ChatGroq wrapper)."""
from typing import Dict, Any, List
from groq import Groq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from config import config
import json
import os

class AgentTools:
    """Collection of tools for the AI Market Analyst agent."""

    def __init__(self, retriever):
        self.retriever = retriever
        # Use direct Groq client
        self.groq_client = Groq(api_key=config.GROQ_API_KEY)

    def _retrieve_context(self, query: str, k: int = 3) -> str:
        """Retrieve relevant context from vector store."""
        docs = self.retriever.get_relevant_documents(query)
        context = "\n\n".join([doc.page_content for doc in docs])
        return context

    def _call_groq(self, messages: List[Dict[str, str]]) -> str:
        """Call Groq API directly."""
        response = self.groq_client.chat.completions.create(
            model=config.GROQ_MODEL,
            messages=messages,
            temperature=0,
            max_tokens=2048
        )
        return response.choices[0].message.content

    def qa_tool(self, question: str) -> str:
        """Answer questions about the market research document."""
        context = self._retrieve_context(question)
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant analyzing a market research document. Answer the user's question based on the provided context. Be specific and cite relevant information. If the answer is not in the context, say so."
            },
            {
                "role": "user",
                "content": f"Context from document:\n{context}\n\nQuestion: {question}\n\nPlease provide a detailed answer."
            }
        ]
        return self._call_groq(messages)

    def summarize_tool(self, aspect: str = "overall") -> str:
        """Summarize market research findings."""
        query_map = {
            "overall": "market research overview findings conclusion",
            "competitors": "competitive landscape market share competitors",
            "swot": "SWOT analysis strengths weaknesses opportunities threats",
            "market_size": "market size growth CAGR projections",
            "recommendations": "strategic priorities recommendations conclusion"
        }
        query = query_map.get(aspect.lower(), "market research summary")
        context = self._retrieve_context(query, k=5)
        messages = [
            {
                "role": "system",
                "content": "You are an expert market analyst. Summarize the key findings from the market research document clearly and concisely. Focus on actionable insights."
            },
            {
                "role": "user",
                "content": f"Document content:\n{context}\n\nPlease provide a comprehensive summary focusing on: {aspect}\n\nStructure with: Key findings, Important metrics, Strategic implications"
            }
        ]
        return self._call_groq(messages)

    def extract_data_tool(self, extraction_type: str = "all") -> Dict[str, Any]:
        """Extract structured data as JSON from the document."""
        context = self._retrieve_context("market research data metrics", k=10)
        messages = [
            {
                "role": "system",
                "content": "You are a data extraction specialist. Extract structured information from the market research document and return ONLY valid JSON with no additional text."
            },
            {
                "role": "user",
                "content": f"""
Document content:
{context}

Extract and return ONLY this JSON structure (no markdown, no extra text):
{{
    "company_name": "string",
    "report_period": "string",
    "flagship_product": "string",
    "market_data": {{
        "current_market_size_billion": 15,
        "projected_market_size_billion": 40,
        "cagr_percentage": 22,
        "projection_year": 2030
    }},
    "market_share": {{
        "innovate_inc": 12,
        "synergy_systems": 18,
        "futureflow": 15,
        "quantumleap": 3
    }},
    "swot": {{
        "strengths": [],
        "weaknesses": [],
        "opportunities": [],
        "threats": []
    }},
    "strategic_priorities": []
}}"""
            }
        ]
        
        response_text = self._call_groq(messages)
        
        try:
            data = json.loads(response_text)
        except json.JSONDecodeError:
            # Try to extract JSON from response
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            if start != -1 and end > start:
                try:
                    data = json.loads(response_text[start:end])
                except:
                    data = {"error": "Failed to parse JSON", "raw_response": response_text}
            else:
                data = {"error": "No JSON found", "raw_response": response_text}
        
        return data
