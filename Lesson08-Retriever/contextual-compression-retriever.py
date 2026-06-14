from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

docs = [
    Document(page_content="The Eiffel Tower is located in Paris, France. It was built in 1889."),
    Document(page_content="Python is a programming language known for its simplicity and readability."),
    Document(page_content="Paris is the capital of France and is famous for its art and culture."),
    Document(page_content="Machine learning is a subset of artificial intelligence."),
]

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
vectorstore = Chroma.from_documents(docs, embeddings)
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
compressor = LLMChainExtractor.from_llm(llm)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever,
)

query = "Where is the Eiffel Tower?"

print(f"\n Query: {query}\n")

# Step 1: Show what the base retriever returns (before compression)
raw_docs = base_retriever.invoke(query)

print("BEFORE COMPRESSION — raw docs from base retriever:")

for i, doc in enumerate(raw_docs, 1):
    print(f"[Doc {i}]: {doc.page_content}")

# Step 2: Show what the compression retriever returns (after compression)
compressed_docs = compression_retriever.invoke(query)

print("\nAFTER COMPRESSION — only relevant snippets:")

for i, doc in enumerate(compressed_docs, 1):
    print(f"[Doc {i}]: {doc.page_content}")


results = compression_retriever.invoke(query)

print("\nFinal Retrieved Results:")
for doc in results:
    print(doc.page_content)
    print("---")
