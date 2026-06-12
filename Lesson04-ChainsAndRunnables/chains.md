### Chains
In LangChain, a Chain is a sequence of steps where the output of one step becomes the input of the next step.


#### Types of chains

1. sequenctial
2. Parallel (RunnableParallel)
3. Conditional (RunnableBranch)




### Runnables
Runnables are the fundamental building blocks.
LCEL (LangChain Expression Language) is the syntax for composing runnables.
Chains are usually just compositions of runnables built using LCEL.

A Runnable is a LangChain component that follows a standard execution interface (invoke, batch, stream, ainvoke) and can be composed with other Runnables to build AI workflows. Prompts, models, retrievers, parsers, and chains are all Runnables in modern LangChain.

A Runnable is the fundamental building block in modern LangChain.
A Runnable is anything that can take an input and produce an output.


Everything follows one common interface:
invoke() : Single input
ainvoke() : Async version of invoke()
batch() : Multiple inputs together
stream() : Streams output token by token


Example : python function as runnable

from langchain_core.runnables import RunnableLambda

def upper(text):
    return text.upper()

runnable = RunnableLambda(upper)

runnable.invoke("hello")


Example: Parallel runnable

from langchain_core.runnables import RunnableParallel

chain = RunnableParallel(
    summary=summary_chain,
    keywords=keyword_chain
)

chain.invoke()
