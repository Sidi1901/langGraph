from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv


load_dotenv()

prompt = PromptTemplate(
    template="Generate 5 interesting facts about {topic}",
    input_variables=["topic"]
)


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=2.0    # temperature must be in the range [0.0, 2.0]
)

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({"topic":"GTA V"})

print(result)

chain.get_graph().print_ascii()