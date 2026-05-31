from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=2.0    # temperature must be in the range [0.0, 2.0]
)

chat_history = [
    SystemMessage(content="You are a senior software developer")
]

while True:
    user_input = input("You: ")
    
    if user_input == "exit":
        break
    
    chat_history.append(HumanMessage(content=user_input))
    result = llm.invoke(chat_history)
    chat_history.append(AIMessage(content=result.content))
    print("AI: ", result.content)