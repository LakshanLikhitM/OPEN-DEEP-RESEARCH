"""
Milestone 2: Multi-Agent System using LangGraph + Groq + Tavily
FIXED:
- Updated Groq model
- Uses .invoke() (no deprecation)
- .env based config
"""

# --------------------------------------------------
# 1. LOAD ENV
# --------------------------------------------------

import os
from dotenv import load_dotenv

load_dotenv()


# --------------------------------------------------
# 2. IMPORTS
# --------------------------------------------------

from typing import TypedDict, List

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from tavily import TavilyClient

# --------------------------------------------------
# 3. SHARED STATE
# --------------------------------------------------

class AgentState(TypedDict):
    user_input: str
    plan: List[str]
    research: List[str]
    final_answer: str


# --------------------------------------------------
# 4. INITIALIZE MODELS (SUPPORTED)
# --------------------------------------------------

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)


tavily = TavilyClient()


# --------------------------------------------------
# 5. PLANNER AGENT
# --------------------------------------------------

def planner_agent(state: AgentState) -> AgentState:
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(
            content=(
                "Break the user query into 3–5 precise research tasks. "
                "Return ONLY a numbered list."
            )
        ),
        HumanMessage(content=state["user_input"])
    ])

    messages = prompt.format_messages()
    response = llm.invoke(messages)

    plan = [
        line.split(".", 1)[-1].strip()
        for line in response.content.split("\n")
        if line.strip()
    ]

    return {**state, "plan": plan}


# --------------------------------------------------
# 6. SEARCHER AGENT
# --------------------------------------------------

def searcher_agent(state: AgentState) -> AgentState:
    research = []

    for task in state["plan"]:
        result = tavily.search(
            query=task,
            search_depth="advanced",
            max_results=3
        )

        for item in result.get("results", []):
            research.append(
                f"Source: {item['title']}\n"
                f"Content: {item['content']}\n"
            )

    return {**state, "research": research}


# --------------------------------------------------
# 7. WRITER AGENT
# --------------------------------------------------

def writer_agent(state: AgentState) -> AgentState:
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(
            content=(
                "Write a concise, factual answer using the research notes. "
                "Do not mention tools or agents."
            )
        ),
        HumanMessage(
            content=(
                f"Question:\n{state['user_input']}\n\n"
                f"Research:\n" + "\n".join(state["research"])
            )
        )
    ])

    messages = prompt.format_messages()
    response = llm.invoke(messages)

    return {**state, "final_answer": response.content}


# --------------------------------------------------
# 8. LANGGRAPH PIPELINE
# --------------------------------------------------

graph = StateGraph(AgentState)

graph.add_node("planner", planner_agent)
graph.add_node("searcher", searcher_agent)
graph.add_node("writer", writer_agent)

graph.set_entry_point("planner")
graph.add_edge("planner", "searcher")
graph.add_edge("searcher", "writer")
graph.add_edge("writer", END)

app = graph.compile()


# --------------------------------------------------
# 9. RUN
# --------------------------------------------------

if __name__ == "__main__":
    query = "Explain how multi-agent systems are used in real-world AI applications"

    result = app.invoke({
        "user_input": query,
        "plan": [],
        "research": [],
        "final_answer": ""
    })

    print("\n========== FINAL ANSWER ==========\n")
    print(result["final_answer"])
    print("\n=================================\n")