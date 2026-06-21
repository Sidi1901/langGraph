from langchain_google_genai  import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv


load_dotenv()


#load the document
loader = TextLoader("docs.txt")

documents = loader.load()

# Split texts into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

docs = text_splitter.split_documents(documents)

# Convert text into embeddings and store in FAISS
vector_store = FAISS.from_documents(docs, GoogleGenerativeAIEmbeddings(model="gemini-embedding-001"))

# Create a retriever
retriever = vector_store.as_retriever()

# Create query
query = input("You:")

retrieved_docs = retriever.invoke(query)

# Combine into single text
retrived_text = "\n".join([doc.page_content for doc in retrieved_docs])

# Initialise the LLM
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=2.0    
)

chat_template = ChatPromptTemplate([
    ("system", "You are a helpful AI agent. Use the following retrieved information to answer the question.\n\n{context}"),
    ("human", "{query}")
])

prompt = chat_template.invoke({"context":retrived_text, "query":query})

answer = model.invoke(prompt)
print(answer.content)