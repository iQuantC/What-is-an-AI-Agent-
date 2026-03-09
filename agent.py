import warnings
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
import math

# Suppress LangGraph deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load LLM
llm = ChatOllama(model="llama3.2")

@tool
def calculator(expression: str) -> str:
    """
    Useful ONLY for mathematical calculations.
    Input must be a valid math expression like:
    2+2, sqrt(16), sin(0.5), etc.
    """
    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            vars(math)
        )
        return str(result)
    except Exception:
        return "Error: Invalid mathematical expression."

tools = [calculator]

# Create agent
agent = create_react_agent(llm, tools)

# Run loop
while True:
    query = input("Ask: ")
    response = agent.invoke({"messages": [{"role": "user", "content": query}]})
    print(response["messages"][-1].content)
