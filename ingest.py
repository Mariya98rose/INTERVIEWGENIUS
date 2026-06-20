# LOAD DOCUMENTS

from langchain_community.document_loaders import DirectoryLoader, TextLoader

loader = DirectoryLoader(
    "dsa_docs",
    glob="**/*.md",
    loader_cls=TextLoader
)

documents = loader.load()

print("Number of documents loaded:", len(documents))
print("\nExample document content:\n")
print(documents[0].page_content[:500])


# SPLIT DOCUMENTS INTO CHUNKS

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print("Number of chunks created:", len(chunks))
print("\nExample chunk:\n")
print(chunks[0].page_content)


# CREATE EMBEDDINGS

from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded")


# CREATE VECTOR DATABASE

from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(chunks, embeddings)

print("Vector database created")


# SAVE DATABASE

vectorstore.save_local("faiss_index")

print("FAISS index saved")