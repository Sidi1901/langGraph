from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# Sample docs 
docs = [
    Document(page_content="Python is a programming language."),
    Document(page_content="LangChain helps build LLM applications."),
    Document(page_content="Chroma is a vector database."),
    Document(page_content="Langchain provides chroma db capabilities.")
]

# Embedding model 
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
)

# Vector store 
# This will generate chroma.db in current directory 
vector_store = FAISS.from_documents(
    documents=docs,
    embedding=embedding_model,
)

# let's perform Similarity Search
# Similarity Search

results = vector_store.similarity_search("What is chroma?", k=2)

print(results)
