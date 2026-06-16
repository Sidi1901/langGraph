from langgraph.graph import StateGraph
from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv 

load_dotenv()


class LLMState(TypedDict):
    question: str 
    answer: str


def llm_qa(state : LLMState) -> LLMState:

    # Extract the question from state
    ques = state['question']

    # Form a prompt
    prompt = f"Answer the following question: {ques}"


    # Ask the question to the LLM


    # Update the answer in the state


# Create a graph
graph = StateGraph(LLMState)

# Add nodes


# Add edges




