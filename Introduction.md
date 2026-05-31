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

5. > 1.2 (OpenAI/Gemini only): Extreme brainstorming or testing boundaries. Proceed with caution, as hallucinations skyrocket here.



