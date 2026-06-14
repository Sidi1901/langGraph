from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.documents import Document
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from dotenv import load_dotenv

load_dotenv()

docs = [
    Document(page_content="Regular walking boosts heart health and can reduce symptoms of depression", metadata={"source":"H1"}),
    Document(page_content="Consuming leafy greens and fruits helps detox the body and improve longevity", metadata={"source":"H2"}),
    Document(page_content="The solar energy system in modern homes can reduce electricity bills and carbon footprint", metadata={"source":"I1"}),
    Document(page_content="Python balances simplicity and power, making it a popular programming language for beginners and experts alike", metadata={"source":"I2"}),
    Document(page_content="Photosynthesis is the process by which plants convert sunlight into chemical energy, sustaining life on Earth", metadata={"source":"I3"}),
    Document(page_content="Deep sleep is crucial for memory consolidation, physical recovery, and overall well-being", metadata={"source":"H3"}),
    Document(page_content="Mindfulness and controlled breathing can reduce stress and improve mental clarity", metadata={"source":"HE1"}),
    Document(page_content="Regular exercise, including strength training and cardio, enhances physical fitness and overall health", metadata={"source":"HE4"}),
]   


# Initialise embedding model
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
)

# Create Choma vector store in-memory
vector_store = FAISS.from_documents(
    documents=docs,
    embedding=embedding_model,
)

# Create retriever
similarity_retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k":5}
)


multiquery_retriever = MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(search_kwargs={"k":3}),
    llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash"),
)

query = "How to improve energy level and maintain balance?"

similarity_result = similarity_retriever.invoke(query)
multiquery_result = multiquery_retriever.invoke(query)

print("Similarity Retriever Results:")
for doc in similarity_result:
    print(f"Source: {doc.metadata['source']}, Content: {doc.page_content}")

print("\nMultiQuery Retriever Results:")
for doc in multiquery_result:
    print(f"Source: {doc.metadata['source']}, Content: {doc.page_content}")

