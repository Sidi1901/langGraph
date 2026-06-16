### Structured Output

Structured Output means getting the LLM's response in a predefined format instead of free-form text.

- Easier for programs to parse.
- Reduces hallucinated formats.
- Ensures required fields are present.
- Useful for APIs, agents, workflows, and automation.


**Example**

Extract information from: "Rahul is 30 years old and lives in Bangalore."

<pre>
Structured Output:

{
  "name": "Rahul",
  "age": 30,
  "city": "Bangalore"
}
</pre>


### LLM Compatibility

There are two types of LLMs with respect to structured output:

1) Those which **can** generate structured output — use functions like `with_structured_output()` in LangChain.
2) Those which **can't** — output parsers can be used as a workaround.


### Implementation Methods

Structured output is commonly implemented using:

1) TypedDict
2) Pydantic
3) JSON Schema


### TypedDict

**What it is**

TypedDict is used to define the expected structure of a dictionary, including its keys and value types. The `typing` module provides the type hints used in TypedDict definitions.

**Limitation:** TypedDict does not perform data validation — it only provides type hints for static analysis tools.

<pre>
+-------------------------------------------+
| EXAMPLE: Using TypedDict                  |
|                                           |
| from typing import TypedDict              |
|                                           |
| class User(TypedDict):                    |
|     name: str                             |
|     age: int                              |
|                                           |
| user: User = {                            |
|     "name": "John",                       |
|     "age": 25                             |
| }                                         |
+-------------------------------------------+
</pre>


### Pydantic

**What it is**

Pydantic provides full data validation on top of type hints. If the data doesn't match the defined schema, Pydantic raises a validation error at runtime — making it a more robust choice than TypedDict when correctness matters.

<pre>
+-------------------------------------------+
| EXAMPLE: Using Pydantic                   |
|                                           |
| from pydantic import BaseModel            |
|                                           |
| class User(BaseModel):                    |
|     name: str                             |
|     age: int                              |
|                                           |
| user = User(name="John", age=25)          |
+-------------------------------------------+
</pre>


Some useful 
1) Optional
2) Literals
