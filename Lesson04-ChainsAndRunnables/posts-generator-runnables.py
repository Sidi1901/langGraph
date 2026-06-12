from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence, RunnableParallel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

prompt1 = PromptTemplate(
    template="Generate short tweet post about {topic}",
    input_variables=["topc"]
)

prompt2 = PromptTemplate(
    template="Generate short linked in post about {topic}",
    input_vaiables=["topic"]
)

parser = StrOutputParser()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

chain = RunnableParallel({
    "tweet": RunnableSequence(prompt1, llm, parser),
    "linkedin" :RunnableSequence(prompt2, llm, parser)
}
)

chain.get_graph().print_ascii()

result = chain.invoke({"topic":"AI"})

print(result)