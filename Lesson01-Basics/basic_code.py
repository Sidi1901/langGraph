from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=5.0    # temperature must be in the range [0.0, 2.0]
)

response = llm.invoke("What is the capital of India?")

print(response.content)


