# What is an AI Agent?

An AI Agent is a system that: 

1. Receives a goal or task
2. Reasons about what to do
3. Uses tools (Search, Calculator, APIs, etc.)
4. Stores memory
5. Takes actions automatically


## Think of it as:
User goal → LLM reasoning → tool usage → memory → result

## Tech Stack
1. Large Language Model (LLM):  Download from Ollama, Hugging Face, Llama (Meta)
2. Agent Frameworks:            LangChain (tool use, chains, agents), LlamaIndex (data retrieval, RAG)
3. Vector Database (memory):    Chroma, FAISS
4. App Interface:               Streamlit (UI for chat apps)
5. Deployment:                  Docker, VMs, Cloud Services


## System Architecture (Standard AI Agent)

User
 ↓
Interface (Streamlit)
 ↓
Agent Framework (LangChain)
 ↓
Local LLM (Ollama + Llama model)
 ↓
Tools
   ├ search
   ├ calculator
   ├ code execution
   └ APIs
 ↓
Memory (Chroma vector DB)


# 1. Let's Demonstrate Tool Use - "Reasoning" and tool Calculator

## Install Ollama (Local LLM Runtime)
Install Ollama
```sh
curl -fsSL https://ollama.com/install.sh | sh
```

Verify Ollama Installation:
```sh
ollama --version
```

Pull your model:
```sh
ollama pull llama3.2
```

Test Ollama runtime:
```sh
ollama run llama3.2
```

Ask a question: What is sqrt(144) + 20?
What is photosynthesis?

"Ctrl + d" or "/bye" to exit 


## Create Python Env
```sh
python3 -m venv ai_agents
source ai_agents/bin/activate
``` 

## Install Packages  in Python Env
```sh
pip install langchain langchain-core langchain-community langchain-ollama langchainhub langgraph chromadb streamlit
```

## Chat AI Agent
This agent: 

1. Answers questions
2. Uses tools
3. Remembers conversations


```sh
ollama serve
ps aux | grep ollama
```

Run llama3.2 on a dedicated terminal:
```sh
ollama run llama3.2
```

Run the Agent:
```sh
python agent.py
```

Ask: What is the sqrt(16)?



