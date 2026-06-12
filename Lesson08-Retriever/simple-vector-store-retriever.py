from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# Sample docs
docs = [
    Document(page_content="Langchain helps developers build LLM application easily"),
    Document(page_content="Chroma is a vector dataabse optimised for LLM searches"),
    Document(page_content="Embeddings convert text into high-dimensional vectors"),
    Document(page_content="OpenAI is one of the powerful embedding models provider"),
]

# Initialise embedding model
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
)

# Create Choma vector store in-memory
vector_store = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    collection_name="my_collection"
)

# Create retriever
retriever = vector_store.as_retriever(search_kwargs={"k":2})

query = "What is Chroma used for?"

results = retriever.invoke(query)

print(results)