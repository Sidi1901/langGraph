### Content

**Foundations**
1. [Large Language Models (LLMs)](#large-language-models-llms)
2. [Token](#token)
3. [Model Params](#model-params)
4. [Prompts](#prompts)

**Data & Retrieval**

5. [Text Splitters](#text-splitters)
6. [Vectors](#vectors)
7. [Retrieval-Augmented Generation (RAG)](#retrieval-augmented-generation-rag)

**Frameworks**

8. [Langchain](#langchain)
9. [LangGraph](#langgraph)

**Agents & Tools**

10. [Tools & Agents](#tools--agents)

**Performance & Optimization**

11. [LLM Inference](#llm-inference)
12. [Long Context vs CAG](#long-context-vs-cag)
13. [Prompt Caching](#prompt-caching)

**Evaluation**

14. [Evals](#evals)

**Memory**

15. [Memory](#memory)

---

### Large Language Models (LLMs)

A Large Language Model is a neural network trained on huge amounts of text to predict the next token in a sequence. Given enough scale (parameters + data + compute), this next-token prediction generalises into abilities like answering questions, writing code, reasoning, and following instructions.

LLMs are stateless between calls — they don't "remember" previous conversations unless the conversation history is explicitly passed back in as part of the prompt/context window.

### Token

A token can be a whole word, a part of a word (like a syllable), or even a single character (like a punctuation mark or an emoji). On average, for standard text:

1 token is approximately 4 characters
1 token is approximately 0.75 words
100 tokens is approximately 75 words

### Model Params

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

#### Top p | Nucleus Sampling
An alternative way to control randomness. Instead of looking at all possible words, the model only considers a pool of top words whose combined mathematical probabilities add up to the value p.
Range: 0.0 to 1.0. (Usually, developers adjust either temperature or top_p, not both at the same time).

top_k is mainly used in Gemini.

#### stop
Pass a list of strings that will tell the model to instantly stop generating text if it types them. Great for parsing structured data. For example, if you want the model to generate a list item, setting stop=["\n"] forces it to stop after completing the first line.

Values: A list of strings, e.g., stop=["END", "###", "\n"].

#### response_format
Tells the model what syntax structure the output must use.
In LangChain, you can pass a dictionary or a Pydantic object. For example: response_format={"type": "json_object"}.

#### streaming
Instead of waiting for the model to generate the entire answer in the background and delivering it all at once, it sends the response token-by-token in real time. Vital for building responsive user interfaces (like ChatGPT) where the user sees words printing out live.

Values: True or False.

safety_settings and thinking_config are used in Gemini.

### Prompts

Prompts can be multi modal - text, images and videos

---

### Text Splitters

A Text Splitter breaks large documents into smaller chunks that can fit within an LLM's context window and be efficiently embedded and retrieved. In LangChain, the most commonly used splitter is RecursiveCharacterTextSplitter, which recursively splits text by paragraphs, sentences, words, and characters while preserving context using chunk overlap.

LLMs have context limits. Suppose you have a 500-page PDF: So you split it into smaller chunks: This process is called text splitting.

1000-page document
        ↓
Too large for LLM
        ↓
Split into chunks

Advantages
1) Context Window Limits
2) Better Retrieval (RAG)
3) Better Embeddings as Embeddings work best on smaller semantic units.

#### Chunk Overlap

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

#### Splitter Types

LangChain provides classes to split text automatically.
1. CharacterTextSplitter : Splits based on character count.
2. RecursiveCharacterTextSplitter : Most Common. It tries multiple separators: It first splits by paragraphs. If a chunk is still too large: then by sentences. If again too large, by words.
3. TokenTextSplitter : Splits based on tokens rather than characters.
4. MarkdownTextSplitter : For Markdown documents.
5. HTMLTextSplitter : For HTML pages.
6. PythonCodeTextSplitter : For source code. Splits around functions and classes.

### Vectors

High-dimensional vectors are the secret sauce behind modern Artificial Intelligence, Machine Learning, and Large Language Models (LLMs). In computer science and mathematics, a vector is simply an ordered list of numbers (often called coordinates or features). The dimensionality is the total number of elements in that list.

Calculating distances across thousands of dimensions requires immense processing power and memory, which is why specialized Vector Databases (like Chroma, Pinecone, or Milvus) are used to handle them efficiently.

#### FAISS
FAISS (Facebook AI Similarity Search) is an open-source library developed by Meta.

FAISS is a vector indexing and nearest-neighbor search library that makes semantic retrieval fast.

When you convert text, images, or audio into data that computers can understand, you turn them into vectors (long lists of numbers generated by machine learning models, often called embeddings).

If you have millions of pieces of text, you get millions of vectors. If a user asks a question, you need to find the text that is most similar to that question by comparing the user's question vector against all millions of stored vectors.

The Naive Way: Compare the question vector to every single vector in your database one by one. If you have 10 million vectors, this is incredibly slow and resource-heavy.

The FAISS Way: FAISS uses advanced math and clustering tricks to find the closest matches in milliseconds, even if you are searching through billions of vectors.

FAISS achieves its incredible speed by utilizing two main concepts: Indexing and Quantization.

1. Vector Clustering (IVF)
Instead of searching the entire database, FAISS groups similar vectors together into clusters (like neighborhoods). When you perform a search, FAISS first figures out which "neighborhood" your query belongs to, and then it only searches within that specific cluster. This cuts down the search space drastically.

2. Vector Compression (Product Quantization)
Vectors take up a lot of memory. FAISS can compress (quantize) these vectors so they take up significantly less RAM, allowing you to store massive datasets entirely in memory for lightning-fast access.

**Why is it used in LangChain?**
If you are building an AI application (like a chatbot that answers questions based on your private company documents), you use FAISS to power the RAG (Retrieval-Augmented Generation) pipeline:

Storage: You chop your documents into paragraphs, convert them into vectors, and store them in a FAISS index.

Retrieval: When a user asks a question, LangChain uses FAISS to instantly find the 3 or 4 paragraphs in your documents that are most relevant to the question.

Generation: LangChain passes those specific paragraphs to the LLM (like GPT or Gemini) so it can write an accurate answer based only on your data.

### Retrieval-Augmented Generation (RAG)

RAG combines retrieval (searching a knowledge base) with generation (the LLM producing an answer), so the model can answer using up-to-date or private data it was never trained on.

Documents → Text Splitter → Embedding Model → Vector Store
User Query → Embedding Model → Similarity Search → Retrieved Chunks
Retrieved Chunks + Query → LLM → Answer

A Retriever wraps a vector store (or other source) to fetch the most relevant chunks for a given query.

---

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
1) Language models - Free form text generation
2) Embedding models - Optimised for multi-turn conversation

### LangGraph

LangGraph is a library (built on top of LangChain) for building stateful, multi-step LLM applications as a graph of nodes and edges, instead of a single linear chain.

Why LangGraph over a plain chain:
1) Workflows can branch (conditional edges), loop (iterative edges), or run steps in parallel — plain chains only go forward.
2) State is explicit and shared across every node, so each step can read/update a common state object.
3) Built-in persistence (checkpointing) lets a graph pause, resume, or replay from any step — useful for human-in-the-loop and long-running agents.

See Lesson12 onward (Sequential, Parallel, Conditional, Iterative workflows, Persistence) for hands-on graph construction.

---

### Tools & Agents

Tools let an LLM call external functions (APIs, calculators, search, databases) instead of relying purely on its own knowledge. The model decides when and with what arguments to call a tool; your code executes it and returns the result back to the model.

Agents are LLMs that can plan, call tools, observe results, and decide on next steps in a loop, rather than producing a single one-shot response.

For multi-step, stateful, or branching agent workflows (sequential / parallel / conditional / iterative graphs with persistence), see LangGraph.

---

### LLM Inference

LLM inference is the process of using a trained Large Language Model (LLM) to generate predictions or responses from new input.

In simple terms:

**Training time compute** → used when building the model (learning weights).
**Inference time compute** (or test-time compute) → used after training when answering user queries.

Test-time compute refers specifically to the amount of computation used during inference.

You type prompt
      ↓
Prompt sent to model
      ↓
Model processes tokens (inference)
      ↓
Model generates output tokens
      ↓
Response displayed

The model: Tokenizes your prompt -> Runs the neural network forward pass -> Predicts the next token repeatedly -> Returns the answer.

All of that is inference.

### Long Context vs CAG

If content is big enough, just skip the retrieval part right?

But it will be too costly.

Also, accuracy drops when context window content increases.

What if you read the document once and then just remember? That's CAG - Cache Augmented Generation.

CAG works with KV cache. This is persisted in some memory like disk memory. Instead of re-reading docs, the model just fetches the KV cache.

CAG works best when source data doesn't change frequently, otherwise cache recomputing will be needed again and again.

### Prompt Caching

Prompt caching is a technique that avoids recomputing parts of a prompt that have already been processed by the LLM.

This can significantly increase speed and reduce cost.

Many applications send the same prefix repeatedly:

-----------------------------
EXAMPLE:
You are an AI code reviewer.

Repository:
<large repository context>

Rules:
<large list of rules>

User question:
How secure is this code?

Then later:

You are an AI code reviewer.

Repository:
<same repository context>

Rules:
<same large list of rules>

User question:
How maintainable is this code?


The first 95% of the prompt is identical.

---

### Evals

#### What are LLM Evals
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

#### Common Metrics
1. Exact Match
- Output must exactly match expected answer.

2. Precision
- How many predicted positives are actually positive

3. Recall
- How many actual positives did we find

#### Scoring Techniques

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

Other evaluations: Hallucination Evaluation, Robustness Evaluation

#### Industry Workflow

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
  "coherence": 5,
}

#### Weaknesses of LLM-as-a-Judge
1. Judge Bias : For example, GPT may prefer GPT-style answers. Score might decrease for different model versions.

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
Questions often require: Physics, Chemistry, Biology at PhD level.

3. HumanEval

Very important for developers.
Created by OpenAI.
Tests code generation.

4. SWE-bench

Extremely important today.
Humans verified issues.
Measures: Can AI fix real GitHub issues?

Today it is one of the most respected coding benchmarks.

Btw, do you know what vibe testing is? XD

#### LLM Application Evals

Because benchmarks evaluate models, while application evals evaluate your entire system.

Industry Trend (2025–2026)

The industry is slowly moving away from Benchmark Scores towards Application-Specific Evals.

---

### Memory

#### Short Term Memory / Context Memory
This is what the model remembers within the current conversation.
Characteristics:

Temporary
Lost when context is removed
Limited by context window size

#### Long Term Memory
Information stored outside the model and retrieved later.
Stored in:

Database
Vector database
Memory service

#### Semantic Memory
Facts and knowledge about the user or world.

Examples:

User likes Python.
User works in Linux Platform Engineering.

#### Procedural Memory
Memory of how to perform tasks.

#### Episodic Memory
Memories of specific events or experiences.
Examples:

Last week user built a Kafka producer.
User discussed DevScore architecture on June 15.

#### Working Memory

The information actively being manipulated while solving a problem.

Example:

Solve:
(10 + 5) × 4

The intermediate values:

10 + 5 = 15
15 × 4 = 60

exist in working memory during reasoning.

Reasoning models spend more compute here.
