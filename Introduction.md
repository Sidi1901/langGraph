### Content

1. [Large Language Models (LLMs)](#LLMs)
2. [Token](#token)
3. [Model Params](#model-params)
4. [Prompts](#prompts)
5. [Text Splitters](#text-splitters)
6. [Vectors](#vectors)
7. [Langchain](#langchain)
8. [LangGraph](#langgraph)
9. [Evals](#evals)
10. [Retrieval-Augmented Generation (RAG)](#retrieval-augmented-generation-rag)
11. [Tools & Agents](#tools--agents)

### Large Language Models (LLMs)

A Large Language Model is a neural network trained on huge amounts of text to predict the next token in a sequence. Given enough scale (parameters + data + compute), this next-token prediction generalises into abilities like answering questions, writing code, reasoning, and following instructions.

LLMs are stateless between calls — they don't "remember" previous conversations unless the conversation history is explicitly passed back in as part of the prompt/context window.

### Token

A token can be a whole word, a part of a word (like a syllable), or even a single character (like a punctuation mark or an emoji).On average, for standard 

1 token is approximately 4 characters
1 token is approximately 0.75 words
100 tokens is approximately 75 words

### MODEL PARAMS:

#### Temperature 
The temperature range is not the same across all models. Every AI provider (Google, OpenAI, Anthropic)

Example:
GoogleGemini -> 0.0 to 2.0
OpenAI -> 0.0 to 2.0
Anthropic ->0.0 to 1.0

**Best Practices Across All Models**
Regardless of which model you are initializing in LangChain, try to map your use case to these general zones rather than maxing out the range:

1. 0.0: Code generation, math, data extraction, JSON generation (strict accuracy required).

2. 0.3 to 0.5: Summarization, QA over documents, factual translation (needs a little writing fluidity but high accuracy).

3. 0.7: General chatbots, email drafting, blogging (the "sweet spot" balance for normal conversations).

4. 1.0: Creative writing, brainstorms, coming up with poem ideas or naming products.

5. Above 1.2 (OpenAI/Gemini only): Extreme brainstorming or testing boundaries. Proceed with caution, as hallucinations skyrocket here.

#### Max Token
Sets a strict cap on the length of the model's response.
Integers (e.g., max_tokens=256 for short answers, or max_tokens=4096 for long-form essays)

#### Top p | Nucleus sampling
An alternative way to control randomness. Instead of looking at all possible words, the model only considers a pool of top words whose combined mathematical probabilities add up to the value p.
Range: 0.0 to 1.0. (Usually, developers adjust either temperature or top_p, not both at the same time).

tpo_k is mainly used in gemini 

#### stop
Pass a list of strings that will tell the model to instantly stop generating text if it types them. Great for parsing structured data. For example, if you want the model to generate a list item, setting stop=["\n"] forces it to stop after completing the first line.

Values: A list of strings, e.g., stop=["END", "###", "\n"].


#### response_format
Tells the model what syntax structure the output must use.
n LangChain, you can pass a dictionary or a Pydantic object. For example: response_format={"type": "json_object"}.

#### streaming
Instead of waiting for the model to generate the entire answer in the background and delivering it all at once, it sends the response token-by-token in real time.Vital for building responsive user interfaces (like ChatGPT) where the user sees words printing out live.

Values: True or False.

safety_settings and thinking_config are used in gemini 

### Prompts

Prompts can be multi modal - text, images and videos

### Text Splitters 

A Text Splitter breaks large documents into smaller chunks that can fit within an LLM's context window and be efficiently embedded and retrieved. In LangChain, the most commonly used splitter is RecursiveCharacterTextSplitter, which recursively splits text by paragraphs, sentences, words, and characters while preserving context using chunk overlap.

LLMs have context limits. Suppose you have a 500-page PDF: So you split it into smaller chunks: This process is called text splitting.

1000-page document
        ↓
Too large for LLM
        ↓
Split into chunks

Addvatages
1) Context Window Limits
2) Better Retrieval (RAG)
3) Better Embeddings as Embeddings work best on smaller semantic units.

Chunk Overlap

Example : Without overlap

Chunk 1:
Kafka is a distributed

Chunk 2:
streaming platform

Meaning gets broken.

Example : With overlap

Chunk 1:
Kafka is a distributed

Chunk 2:
is a distributed streaming platform

Some context is preserved.

### Vectors
High-Dimensional Vectors

High-dimensional vectors are the secret sauce behind modern Artificial Intelligence, Machine Learning, and Large Language Models (LLMs). In computer science and mathematics, a vector is simply an ordered list of numbers (often called coordinates or features). The dimensionality is the total number of elements in that list.

Calculating distances across thousands of dimensions requires immense processing power and memory, which is why specialized Vector Databases (like Chroma, Pinecone, or Milvus) are used to handle them efficiently.

### Langchain

LangChain is a framework/library used to build applications powered by Large Language Models (LLMs).
Instead of writing everything manually, LangChain gives reusable building blocks.

1) It supports major LLMs.
2) Open Source, etc

Example use cases:

Chatbots, RAG applications, AI agents, Document Q&A and Multi-step AI workflows.

langchain-workspace/
├── langchain-core/       # Core interfaces, base classes, and data types
├── langchain-community/  # Third-party integrations (OpenAI, HuggingFace, Pinecone, etc.)
└── langchain/            # Advanced chains, agents, and application logic architecture

Provides two types of models
1) language models - Free from text generation
2) Embedding models - Optimised for multi-turn conversation

### LangGraph

LangGraph is a library (built on top of LangChain) for building stateful, multi-step LLM applications as a graph of nodes and edges, instead of a single linear chain.

Why LangGraph over a plain chain:
1) Workflows can branch (conditional edges), loop (iterative edges), or run steps in parallel — plain chains only go forward.
2) State is explicit and shared across every node, so each step can read/update a common state object.
3) Built-in persistence (checkpointing) lets a graph pause, resume, or replay from any step — useful for human-in-the-loop and long-running agents.

See Lesson12 onward (Sequential, Parallel, Conditional, Iterative workflows, Persistence) for hands-on graph construction.

### Evals

#### What is LLM evals
Just like unit tests verify software behavior, LLM evals verify AI behavior.

Dataset + Prompt + Model + Metric = Score

The biggest challenge is that LLM outputs are probabilistic, so exact matching often isn't enough. That's why modern evaluation systems increasingly rely on LLM-as-a-Judge, pairwise comparisons, and human-reviewed golden datasets.

Evaluation Pipeline → automated system that runs those evals repeatedly and tracks results

A benchmark is a standardized dataset + rules + scoring method that allows everyone to compare models fairly.

#### Types
1. Reference-Based Evals 
- You already know the correct answer
- Compare expected vs actual

2. Reference-Free Evals
- Need another LLM or human to judge

#### Common metrics
1. Exact Match
- Output must exactly match expected answer.

2. Precision
- How many predicted positives are actually positive

3. Recall
- How many actual positives did we find

**Scoring techniques**

F1 score
score = 2 × Precision × Recall

LLM-as-a-Judge
Heavily used by LangSmith, DeepEval, Braintrust, Phoenix

Pairwise Evaluation
Instead of absolute scoring, Compare two outputs.

Human Evaluation
Human evaluates Correctness, Clarity, Usefulness, Safety. Expensive but highest quality.

Regression Testing
Prompt v1 -> Score = 90%
You improved prompt.
Prompt v2 -> Score = 85%


Other evalusations Hallucination Evaluation, Robustness Evaluation

Industry Workflow

Create Golden Dataset -> Run Model -> Calculate Metrics -> Store Result -> Compare Against Previous Version -> Deploy If Better


#### Multi-Metric Evaluation

Most production systems don't use one score.

They use multiple dimensions.

Example:

{
  "correctness": 9,
  "relevance": 8,
  "completeness": 7,
  "clarity": 9,
  "faithfulness": 8,
  "coherence":5,
}

#### Weaknesses of LLM-as-a-Judge
1. Judge Bias : For example, GPT may prefer GPT-style answers. score might decrease for different model version

2. Hallucinating Judge : Judge can also be wrong. It is still an LLM.

3. Cost : Evaluation can cost more than inference.

#### Benchmarks
Most benchmarks fall into:

Knowledge
Reasoning
Coding
Math
Science
Agent
Software Engineering
Safety

1. MMLU = Massive Multitask Language Understanding
What it measures: General knowledge

2. GPQA

Graduate-level science benchmark.

Much harder than MMLU.
Questions often require:Physics Chemistry Biology at PhD level.

3. HumanEval

Very important for developers.
Created by OpenAI.
Tests code generation.


8. SWE-bench

Extremely important today.
Humans verified issues.
Measures: Can AI fix real GitHub issues?


Today it is one of the most respected coding benchmarks.

Btw, do you know what is vibe testing? XD

#### LLM Application Evals

Because benchmarks evaluate models, while application evals evaluate your entire system.

Industry Trend (2025–2026)

The industry is slowly moving away from Benchmark Scores towards Application-Specific Evals

### Retrieval-Augmented Generation (RAG)

RAG combines retrieval (searching a knowledge base) with generation (the LLM producing an answer), so the model can answer using up-to-date or private data it was never trained on.

Documents → Text Splitter → Embedding Model → Vector Store
User Query → Embedding Model → Similarity Search → Retrieved Chunks
Retrieved Chunks + Query → LLM → Answer

A Retriever wraps a vector store (or other source) to fetch the most relevant chunks for a given query.

### Tools & Agents

Tools let an LLM call external functions (APIs, calculators, search, databases) instead of relying purely on its own knowledge. The model decides when and with what arguments to call a tool; your code executes it and returns the result back to the model.

Agents are LLMs that can plan, call tools, observe results, and decide on next steps in a loop, rather than producing a single one-shot response.

For multi-step, stateful, or branching agent workflows (sequential / parallel / conditional / iterative graphs with persistence), see LangGraph.
