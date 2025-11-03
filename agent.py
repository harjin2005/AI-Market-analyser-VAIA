"""Agentic AI routing using LangGraph for autonomous tool selection."""
from typing import TypedDict, Literal, List, Dict, Any
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, END
from config import config
from tools import AgentTools
import json

class AgentState(TypedDict):
    """State schema for the agent graph."""
    messages: List[Dict[str, str]]
    next_action: str

class MarketAnalystAgent:
    """Autonomous agent that routes queries to appropriate tools using LangGraph."""

    def __init__(self, retriever):
        self.agent_tools = AgentTools(retriever)
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build the LangGraph workflow with autonomous routing."""
        
        def router_node(state: AgentState) -> AgentState:
            """Intelligent router that decides which tool to use."""
            if not state["messages"]:
                return state
            
            last_message = state["messages"][-1]["content"].lower()
            
            # Route based on query content
            if any(word in last_message for word in ["extract", "json", "data", "structure"]):
                state["next_action"] = "extract"
            elif any(word in last_message for word in ["summarize", "summary", "overview"]):
                state["next_action"] = "summarize"
            else:
                state["next_action"] = "qa"
            
            return state

        def qa_tool_node(state: AgentState) -> AgentState:
            """Q&A tool node."""
            if not state["messages"]:
                return state
            query = state["messages"][-1]["content"]
            response = self.agent_tools.qa_tool(query)
            state["messages"].append({"role": "assistant", "content": response})
            return state

        def summarize_tool_node(state: AgentState) -> AgentState:
            """Summarization tool node."""
            if not state["messages"]:
                return state
            query = state["messages"][-1]["content"]
            aspect = "overall"
            if "competitor" in query.lower():
                aspect = "competitors"
            elif "swot" in query.lower():
                aspect = "swot"
            response = self.agent_tools.summarize_tool(aspect)
            state["messages"].append({"role": "assistant", "content": response})
            return state

        def extract_tool_node(state: AgentState) -> AgentState:
            """Data extraction tool node."""
            data = self.agent_tools.extract_data_tool()
            response = json.dumps(data, indent=2)
            state["messages"].append({"role": "assistant", "content": response})
            return state

        def route_decision(state: AgentState) -> Literal["qa", "summarize", "extract", "end"]:
            """Conditional routing based on agent decision."""
            action = state.get("next_action", "end")
            return action

        # Build the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("router", router_node)
        workflow.add_node("qa", qa_tool_node)
        workflow.add_node("summarize", summarize_tool_node)
        workflow.add_node("extract", extract_tool_node)
        
        # Set entry point
        workflow.set_entry_point("router")
        
        # Add conditional edges (routing logic)
        workflow.add_conditional_edges(
            "router",
            route_decision,
            {
                "qa": "qa",
                "summarize": "summarize",
                "extract": "extract",
                "end": END
            }
        )
        
        # All tool nodes lead to END
        workflow.add_edge("qa", END)
        workflow.add_edge("summarize", END)
        workflow.add_edge("extract", END)
        
        return workflow.compile()

    def process_query(self, query: str) -> str:
        """Process a user query through the agentic workflow."""
        print(f"🤖 Processing query through LangGraph agent...")
        initial_state = {
            "messages": [{"role": "user", "content": query}],
            "next_action": ""
        }
        
        result = self.graph.invoke(initial_state)
        
        # Extract final response
        if result["messages"]:
            last_message = result["messages"][-1]
            if isinstance(last_message, dict):
                return last_message.get("content", "No response")
            return str(last_message)
        return "No response generated"

    def process_query_with_history(self, messages: List[Dict[str, str]]) -> str:
        """Process query with conversation history."""
        if not messages:
            return "No query found"
        
        initial_state = {
            "messages": messages,
            "next_action": ""
        }
        
        result = self.graph.invoke(initial_state)
        
        if result["messages"]:
            last_message = result["messages"][-1]
            if isinstance(last_message, dict):
                return last_message.get("content", "No response")
            return str(last_message)
        return "No response generated"
