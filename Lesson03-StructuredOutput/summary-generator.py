# By using Str output parser. See how chains are used effectively by using string output parser

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

template1 = PromptTemplate(
    template="Write a detailed topic on {topic}",
    input_variables=["topic"]
)


template2 = PromptTemplate(
    template="Write 5 line summary on the text/n {text}",
    input_variables=["text"]
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=2.0    # temperature must be in the range [0.0, 2.0]
)

parser = StrOutputParser()

chain = template1 | llm | parser | template2 | llm | parser

result = chain.invoke({"topic":"black hole"})

print(result)