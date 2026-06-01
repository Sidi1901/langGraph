# By using TypedDict and Annotated for structured output, we can define a clear schema for the output of our language model. This allows us to easily parse and utilize the generated content in a structured way.

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional, Literal


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=2.0    # temperature must be in the range [0.0, 2.0]
)

class Review(TypedDict):
    rating: Annotated[int, "out of 10 rating, if cons is empty give ratign 10"]
    pros: Annotated[str, "brief good part"]
    cons: Annotated[str, "brief negative part"]
    user_gender: Annotated[Optional[str],"Tell gender"]
    is_adult: Annotated[Literal["yes","no"], "customer is adult or not"]

structured_output = llm.with_structured_output(Review)

result = structured_output.invoke("The hardware is soo great")

print(result)
