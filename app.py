import streamlit as st
import os
from groq import Groq

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


# ---------------------------------------
# INITIALIZE GROQ CLIENT
# ---------------------------------------

client = Groq(api_key=os.environ["GROQ_API_KEY"])


# ---------------------------------------
# LOAD EMBEDDING MODEL
# ---------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ---------------------------------------
# LOAD FAISS VECTOR DATABASE
# ---------------------------------------

vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)


# ---------------------------------------
# STREAMLIT UI
# ---------------------------------------

st.title("InterviewGenius – DSA Interview Assistant")

st.write(
    "Ask questions about Data Structures and Algorithms. "
    "The assistant retrieves relevant algorithm patterns from the knowledge base."
)


# ---------------------------------------
# CHAT MEMORY
# ---------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# DISPLAY PREVIOUS MESSAGES

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# ---------------------------------------
# USER INPUT
# ---------------------------------------

query = st.chat_input("Ask a DSA question")


if query:

    # SHOW USER MESSAGE
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.write(query)


    # ---------------------------------------
    # RETRIEVE RELEVANT DOCUMENTS
    # ---------------------------------------

    docs = vectorstore.similarity_search(query, k=3)

    context = "\n\n".join([doc.page_content for doc in docs])


    prompt = f"""
You are an expert tutor for Data Structures and Algorithms interviews.

Use the context to answer the question clearly.

Context:
{context}

Question:
{query}

Instructions:
1. Identify the algorithmic pattern (Sliding Window, Binary Search, etc).
2. Explain the concept simply.
3. Walk through the reasoning step-by-step.
"""


    # ---------------------------------------
    # GENERATE ANSWER WITH GROQ
    # ---------------------------------------

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a DSA tutor helping students prepare for coding interviews."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    answer = response.choices[0].message.content


    # DISPLAY ANSWER

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.write(answer)


    # OPTIONAL: SHOW RETRIEVED CONTEXT

    with st.expander("Retrieved context from knowledge base"):
        for doc in docs:
            st.write(doc.page_content)
            st.write("---")