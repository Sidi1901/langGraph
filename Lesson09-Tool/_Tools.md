### Content



### What is a tool


Tools are nothing but functions

An AI agent is LLM powered system that can autonomously think, decide and take actions using external APIs to achieve a goal.

Langchain also provides built-in tools.

#### Custom tools

Ways to create a custom tool
1. Decorator 
2. StructuredTool and pydantic
3. BaseTool class


#### Decorator @tool

1. Create Function
2. Add decorator '@tool'


#### StructuredTool and pydantic

Good for strict type checking and constraint using pydantic.

#### BaseTool

BaseTool is the abstract base class for all tools in langchain

All other tool types like @tool and StructuredTool are built on top of BaseTool.

#### Best pratices
Provide docstrings <- highly recommened
Do type hinting


tool.name shows tool name
tool.description shows tooldescription
tool.args shows arguments info
tool.args_schema.model_json_schema


### Tool calling

#### Tool Binding
It is the step where we register tool with LLM so that,
1. The LLM knows what tools are available.
2. It knows what each tool does.
3. It knows what input format to use.

Not all LLMs supports tool binding

Note: LLM itself doesn't do execution of tool. Execution is handled by programmer/langchain.


#### ToolMessage

Other that SystemMessage, AIMessage, HumanMessage, there is toolMessage.




