# Using pydantic

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional, Literal


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=2.0
)

class Review(BaseModel):
    rating: int = Field(description="out of 10 rating, if cons is empty give rating 10")
    pros: str = Field(description="brief good part")
    cons: str = Field(description="brief negative part")
    user_gender: Optional[str] = Field(description="Tell gender")
    is_adult: Literal["yes", "no"] = Field(description="customer is adult or not")

structured_output = llm.with_structured_output(Review)

result = structured_output.invoke("The hardware is soo great")

print(result)
