### Messages

Three types of messages

1) System message
2) Human message
3) AI message

**SystemMessage**
The Role: Sets the foundational instructions, persona, operational boundaries, and system rules for the model.

Behavior: The LLM processes this message first and treats it with high priority throughout the life of the session. It is hidden from the end-user and defines how the model must behave.

**HumanMessage**
The Role: Represents the input coming directly from the end-user.

Behavior: This contains the actual prompt, question, task request, or data payload that the user expects the model to process.

**AIMessage**
The Role: Represents the output generated back by the assistant/model.

Behavior: In simple single-turn requests, this is what the model returns to you. In multi-turn chat architectures, you pass past AIMessages back into the input list so the model can reference what it said previously, acting as the conversation's memory.


### Templates

**LLM Prompt template - PromptTemplate**

A PromptTemplate is used to create a string-based prompt blueprint for traditional, single-string completion models. It uses named placeholders inside curly braces {} to dynamicize your inputs, turning a static text string into a reusable function that accepts variables at runtime.


**Chat Prompt template - ChatPromptTemplate**

A ChatPromptTemplate is an advanced template designed for Chat Models that expect an explicit array of structured messages rather than a single block of raw text. It allows you to organize multiple role-based templates (such as system instructions, historical placeholder structures, and human inputs) into a structured list that mirrors the real-time chat lifecycle


<pre>
+---------------------------------------------------------------------------------------+
| EXAMPLE: Using PromptTemplate                                                         |
|                                                                                       |
| from langchain_core.prompts import PromptTemplate                                     |
|                                                                                       |
| # 1. Define a string blueprint with a variable placeholder                            |
| template = "Provide a high-level summary of the following log: {log}"                 |
| prompt_template = PromptTemplate.from_template(template)                              |
|                                                                                       |
| # 2. Format the template into a plain string at runtime                               |
| final_prompt = prompt_template.format(log="CRITICAL: OOM Killer run")                 |
|                                                                                       |
| print(final_prompt)                                                                   |               
| # Output: Provide a high-level summary of the following log: CRITICAL: OOM Killer run |
+---------------------------------------------------------------------------------------+

+--------------------------------------------------------------------------------+
| EXAMPLE: Using ChatPromptTemplate                                              |
|                                                                                |
| from langchain_core.prompts import ChatPromptTemplate                          |
|                                                                                |
| # 1. Create a structured multi-role blueprint                                  |
| chat_template = ChatPromptTemplate.from_messages([                             |         
|     ("system", "You are an expert platform assistant specialized in {topic}."),|
|     ("human", "Analyze this error: {error_msg}")                               |
| ])                                                                             |
|                                                                                |
| # 2. Format variables into a validated list of Chat Message objects            |
| formatted_messages = chat_template.format_messages(                            |
|     topic="Kubernetes Networking",                                             |
|     error_msg="CrashLoopBackOff on CoreDNS pod"                                |
| )                                                                              |
+--------------------------------------------------------------------------------+

</pre>


We will be using ChatPromptTemplate in examples.
