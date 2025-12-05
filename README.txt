
AI Research Chatbot (LangGraph + Groq + Tavily + Streamlit)

This project implements a simple research-oriented chatbot built using LangGraph, Groq LLMs, Tavily web search, and Streamlit.
The goal is to take a user question, break it into smaller research tasks, search the web for each task, and produce a clear final answer.

This project is mainly intended for learning how to build a multi-agent pipeline.

Overview

The chatbot follows a three-agent architecture:

1. Planner Agent
   Breaks the user query into 3–5 research tasks.

2. Searcher Agent
   Uses the Tavily API to search the internet for each task and collects relevant information.

3. Writer Agent
   Reads all the collected research and generates a final answer using Groq’s Llama 3.1 8B Instant model.

A Streamlit interface is provided for chatting with the system.

Project Structure

multiagent.py   - Contains all agents and the LangGraph pipeline
app.py          - Streamlit interface
.env            - Stores API keys
README.md       - Documentation

Setup Instructions

1. Clone the repository:
   git clone <your-repository-url>
   cd <project-folder>

2. Install dependencies:
   pip install -r requirements.txt

3. Create a .env file and add your API keys:
   GROQ_API_KEY=your-groq-key
   TAVILY_API_KEY=your-tavily-key

4. Run the Streamlit app:
   streamlit run app.py

How the System Works

Planner Agent:
Reads the user question and breaks it into a list of tasks.

Searcher Agent:
Uses Tavily Search to fetch information related to each task.

Writer Agent:
Synthesizes the research and produces a readable final answer.

The LangGraph pipeline follows this order:
Planner → Searcher → Writer → End

Streamlit Interface

The interface behaves like a chat application and displays:
- User messages
- Assistant responses
- Research-backed final answers

Example Usage

Example question:
Explain how machine learning is used in weather forecasting.

The system will break it into tasks, perform searches, and provide a structured answer.

Requirements

langchain
langgraph
langchain-groq
tavily-python
streamlit
python-dotenv

Notes

This project is designed for experimentation and learning. You can extend it with memory, more agents, or UI improvements.

Contributing

Suggestions and contributions are welcome.

