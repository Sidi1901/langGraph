"""

As Chat Models are used more than direct models, it is important to understand how to use them effectively.

Using chatPromptTemplate and chat_history.txt for storing messages


"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv


load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=2.0    # temperature must be in the range [0.0, 2.0]
)


chat_template = ChatPromptTemplate([
    ("system", "You are a helpful customer support agent"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human","{query}")
])

chat_history = []

with open("chat_history.txt") as f:
    chat_history.extend(f.readlines())

while True:
    user_input = input("You: ")
    if user_input == "exit":
        break
    prompt = chat_template.invoke({"chat_history":chat_history, "query":user_input})
    result = llm.invoke(prompt)
    chat_history.append(f'HumanMessage(content="{user_input}")')
    chat_history.append(f'AIMessage(content="{result.content}")')
    print(result.content)

with open("chat_history.txt", "w") as f:
    for content in chat_history:                                              
       clean_content = content.replace("\n", " ")                                  
       f.write(f"{clean_content}\n")    

print("--- Session saved successfully ---")


"""
You: Is my refund completed?
Your refund was **initiated** on April 26, 2026. This means the process has begun on our end.

It is not yet completed. Typically, once initiated, refunds can take **5-7 business days** to fully process and appear in your account, depending on your bank.

You should receive a notification once the refund is fully processed and the funds are on their way.
--- Session saved successfully ---

"""