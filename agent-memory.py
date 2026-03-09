import math
import warnings
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

warnings.filterwarnings("ignore", category=DeprecationWarning)


# Load LLM
llm = ChatOllama(model="llama3.2")

# Setup Memory (Vector DB)
embeddings = OllamaEmbeddings(model="llama3.2")

vector_store = Chroma(
    collection_name="agent_memory",
    embedding_function=embeddings,
    persist_directory="./memory_db"
)


# Conversation History
chat_history = []


# Tool: Calculator
def safe_calculate(expression: str):
    try:
        result = eval(expression, {"__builtins__": {}}, vars(math))
        return str(result)
    except:
        return None


# Chat Loop
while True:
    query = input("\nAsk: ")

    math_result = safe_calculate(query)
    if math_result is not None:
        print(f"Answer: {math_result}")
        continue

    # Retrieve memory
    docs = vector_store.similarity_search(query, k=3)

    memory_context = ""
    if docs:
        memory_context = "\nRelevant past memories:\n"
        for doc in docs:
            memory_context += f"- {doc.page_content}\n"

    # Build prompt
    prompt = f"""
You are a helpful AI assistant with long-term memory.

{memory_context}

Conversation history:
{chat_history}

User: {query}
Assistant:
"""

    # Get response
    response = llm.invoke(prompt)
    assistant_text = response.content

    print(f"Assistant: {assistant_text}")

    # Update history
    chat_history.append(f"User: {query}")
    chat_history.append(f"Assistant: {assistant_text}")

    # Store memory
    memory_entry = f"User: {query}\nAssistant: {assistant_text}"
    vector_store.add_documents([Document(page_content=memory_entry)])
    vector_store.persist()
