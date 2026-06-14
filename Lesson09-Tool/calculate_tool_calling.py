from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()



@tool
def multiply(a:int,b:int)->int:
    """Multiply two numbers"""
    return a*b


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

llm_with_tools = llm.bind_tools([multiply])

# No tool calling
result = llm_with_tools.invoke("Hi How are you?")

print(result)

# Tool calling

result = llm_with_tools.invoke("Calculate 3 multiply 10?")

print(result)

tool_result = multiply.invoke(result.tool_calls[0])

print(tool_result)