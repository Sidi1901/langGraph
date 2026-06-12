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



