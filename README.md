# InterviewGenius – DSA Interview Assistant

A Retrieval-Augmented Generation (RAG) chatbot that helps you prepare for Data Structures and Algorithms interviews. Ask it a question, and it retrieves relevant algorithm patterns from a local knowledge base before generating a clear, step-by-step explanation.

## How It Works

1. **Knowledge base** – Markdown notes on DSA patterns (Sliding Window, Two Pointers, Dynamic Programming, etc.) live in `dsa_docs/`.
2. **Ingestion** (`ingest.py`) – Loads those docs, splits them into chunks, embeds them using a HuggingFace sentence-transformer model, and stores them in a local FAISS vector index.
3. **Chat app** (`app.py`) – A Streamlit interface that takes your question, retrieves the most relevant chunks from FAISS, and passes them as context to a Groq-hosted LLaMA 3.3 model to generate a tutor-style answer.

## Tech Stack

- **Streamlit** – chat interface
- **Groq** – LLM inference (`llama-3.3-70b-versatile`)
- **LangChain** – document loading, splitting, and vector store integration
- **FAISS** – local vector similarity search
- **HuggingFace `sentence-transformers/all-MiniLM-L6-v2`** – embeddings

## Project Structure

```
INTERVIEWGENIUS/
├── app.py              # Streamlit chat app
├── ingest.py            # Builds the FAISS index from dsa_docs/
├── dsa_docs/             # Markdown notes on DSA patterns (+ images)
├── requirements.txt
└── .gitignore
```

> Note: `faiss_index/` (the generated vector index) and `venv/` are not tracked in this repo — see Setup below to regenerate them.

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Mariya98rose/INTERVIEWGENIUS.git
cd INTERVIEWGENIUS
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your Groq API key

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_actual_key_here
```

Get a free key at [console.groq.com](https://console.groq.com).

### 5. Build the vector index

This reads everything in `dsa_docs/` and creates the local `faiss_index/` folder:

```bash
python ingest.py
```

### 6. Run the app

```bash
streamlit run app.py
```

The app will open in your browser, ready to answer DSA questions.

## Usage

Type a question like:

> "How do I detect a cycle in a linked list?"

The assistant will:
1. Identify the relevant pattern (e.g. Fast & Slow Pointers)
2. Explain the concept
3. Walk through the reasoning step-by-step

You can also expand **"Retrieved context from knowledge base"** under any answer to see exactly which notes were used to generate it.

## Adding More Patterns

Drop new `.md` files into `dsa_docs/`, then re-run:

```bash
python ingest.py
```

This rebuilds the FAISS index to include the new content.

## Roadmap / Ideas

- [ ] Add source citations inline in the chat response
- [ ] Support code execution for practicing solutions
- [ ] Deploy to Streamlit Community Cloud
