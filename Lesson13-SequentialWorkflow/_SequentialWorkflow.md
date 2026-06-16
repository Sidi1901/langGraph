
#### Pydantic vs TypedDict

In LangGraph, the state is passed around between nodes constantly. TypedDict is the standard choice here because it is a lightweight, native Python type hint that doesn't enforce runtime validation by default.

Pydantic is a data validation library. You should use it when you need strict enforcement, data serialization, or when interacting with LLMs for structured output.

You can actually use a Pydantic model as your LangGraph state if you want strict validation at every node transition. However, because LangGraph frequently shallow-copies and updates state, using a Pydantic model can sometimes feel clunky compared to a native TypedDict. For 90% of LangGraph projects, stick to TypedDict for state.