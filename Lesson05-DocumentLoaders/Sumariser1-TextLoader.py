from langchain_community.document_loaders import TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# load document 

loader = TextLoader("sample1.txt")

docs = loader.load()

prompt = PromptTemplate(
    template="Give two line summary about {text}",
    input_variables=["text"]
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

parser = StrOutputParser()

chain = prompt | llm | parser 

result = chain.invoke({"text":docs[0].page_content})

print(result)