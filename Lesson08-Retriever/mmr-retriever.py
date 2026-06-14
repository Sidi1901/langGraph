from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# Sample docs
docs = [
    Document(page_content="Langchain make it easy to work with LLM"),
    Document(page_content="Langchain is used to build LLM based applications"),
    Document(page_content="Chroma is used to store and search document embeddings"),
    Document(page_content="Embeddngs are vector representations of text"),
    Document(page_content="MMR is a technique to select relevant documents based on relevance and diversity"),
    Document(page_content="Langchain supports chroma, FAISS, Pinecone and more vector stores"),
]

# Initialise embedding model
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
)

# Create Choma vector store in-memory
vector_store = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
)

# Create retriever
retriever = vector_store.as_retriever(
    search_type="mmr", # Try with search_type="similarity"
    search_kwargs={"k":3}
)

query = "What is langchain?"

results = retriever.invoke(query)

print(results)