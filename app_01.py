import math
import warnings
import streamlit as st
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Streamlit Page Configuration
st.set_page_config(page_title="AI Memory Agent", layout="centered")
st.title("AI Memory-Enabled Assistant")


# Load LLM (cached)
@st.cache_resource
def load_llm():
    return ChatOllama(model="llama3.2")

llm = load_llm()


# Setup Vector Memory (cached)
@st.cache_resource
def load_vector_store():
    embeddings = OllamaEmbeddings(model="llama3.2")
    return Chroma(
        collection_name="agent_memory",
        embedding_function=embeddings,
        persist_directory="./memory_db"
    )

vector_store = load_vector_store()


# Session State for Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Clear Memory Button
col1, col2 = st.columns([4, 1]) 

with col2:
    if st.button("Clear Memory"):
        vector_store.delete_collection()  # delete vector DB
        st.cache_resource.clear()         # clear cached DB
        st.session_state.chat_history = []
        st.success("Memory cleared!")
        st.rerun()


# Calculator tool
def safe_calculate(expression: str):
    try:
        result = eval(expression, {"__builtins__": {}}, vars(math))
        return str(result)
    except:
        return None


# Display Previous Messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat Input
if prompt := st.chat_input("Ask something..."):

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.chat_history.append(
        {"role": "user", "content": prompt}
    )

    # Calculator check
    math_result = safe_calculate(prompt)
    if math_result is not None:
        response_text = f" **Answer:** {math_result}"
    else:
        # Retrieve memory
        docs = vector_store.similarity_search(prompt, k=3)

        memory_context = ""
        if docs:
            memory_context = "\nRelevant past memories:\n"
            for doc in docs:
                memory_context += f"- {doc.page_content}\n"

        full_prompt = f"""
You are a helpful AI assistant with long-term memory.

{memory_context}

Conversation history:
{st.session_state.chat_history}

User: {prompt}
Assistant:
"""

        response = llm.invoke(full_prompt)
        response_text = response.content

        # Store memory
        memory_entry = f"User: {prompt}\nAssistant: {response_text}"
        vector_store.add_documents([Document(page_content=memory_entry)])
        vector_store.persist()

    with st.chat_message("assistant"):
        st.markdown(response_text)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": response_text}
    )
