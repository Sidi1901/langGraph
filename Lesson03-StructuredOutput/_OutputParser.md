### Output Parsers

Output parsers are used when the LLM does **not** natively support structured output. They work by instructing the model (via the prompt) to respond in a specific format, then parsing the raw text response into a structured Python object.

This is the fallback approach for models that lack `with_structured_output()` support.


### How It Works

1) A format instruction string is generated from the parser and injected into the prompt.
2) The LLM returns a text response that follows the requested format.
3) The parser converts that raw text into a Python object.


### StrOutputParser

**What it is**

The simplest parser — extracts the plain string content from the LLM's response message. It strips away the message wrapper (`AIMessage`) and returns just the text.

**When to use:** When you only need the raw text reply and no further structure.

<pre>
+-----------------------------------------------------------+
| EXAMPLE: Using StrOutputParser                            |
|                                                           |
| from langchain_core.output_parsers import StrOutputParser |
|                                                           |
| parser = StrOutputParser()                                |
|                                                           |
| chain = llm | parser                                      |
|                                                           |
| result = chain.invoke("Tell me a joke")                   |
| print(result)  # plain string, no AIMessage wrapper       |
+-----------------------------------------------------------+
</pre>


### PydanticOutputParser

**What it is**

Instructs the LLM to respond in a JSON format that matches a Pydantic model, then validates and parses the response into that model. The parser automatically generates format instructions that are injected into the prompt.

**When to use:** When you need structured, validated output from a model that does not support `with_structured_output()`.

<pre>
+------------------------------------------------------------------+
| EXAMPLE: Using PydanticOutputParser                              |
|                                                                  |
| from langchain_core.output_parsers import PydanticOutputParser   |
| from langchain_core.prompts import PromptTemplate                |
| from pydantic import BaseModel, Field                            |
|                                                                  |
| class Review(BaseModel):                                         |
|     summary: str = Field(description="brief summary")           |
|     rating: int  = Field(description="score out of 10")         |
|                                                                  |
| parser = PydanticOutputParser(pydantic_object=Review)            |
|                                                                  |
| prompt = PromptTemplate(                                         |
|     template="Answer the query.\n{format_instructions}\n{query}",|
|     input_variables=["query"],                                   |
|     partial_variables={                                          |
|         "format_instructions": parser.get_format_instructions()  |
|     }                                                            |
| )                                                                |
|                                                                  |
| chain  = prompt | llm | parser                                   |
| result = chain.invoke({"query": "Review: great build quality"})  |
|                                                                  |
| print(result.summary)                                            |
| print(result.rating)                                             |
+------------------------------------------------------------------+
</pre>

### JsonOutputParser 

JsonOutputParser is a built-in tool designed to take a raw text response from a Large Language Model (LLM) and parse it into a structured JSON object

*Can you exaplain the difference between PydanticOutputParser and JsonOutputParser and when to use what btw?*

### Comparison

| | StrOutputParser | PydanticOutputParser |
|---|---|---|
| Output type | `str` | Pydantic model instance |
| Validation | None | Full Pydantic validation |
| Needs prompt injection | No | Yes (`get_format_instructions()`) |
| Use case | Plain text replies | Structured, validated data |


**.with_structured_output() is preferred** 

In LangChain and LangGraph, using with_structured_output is objectively better and is the recommended modern standard.

The core difference comes down to how the structure is enforced:

OutputParsers (The Prompt-Based Way): The parser injects raw text formatting instructions (like "Return your answer as a valid JSON matching this schema...") into your prompt. The LLM generates standard text, and LangChain tries to parse that text string after the fact.

.with_structured_output() (The Native Way): It bypasses prompt-level begging. It binds directly to the model's native API (like OpenAI's JSON Mode/Structured Outputs, Anthropic's Tool Calling, or Gemini's Function Calling). The model is constrained at the token generation level to output valid structures.

