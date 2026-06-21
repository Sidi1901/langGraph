# LangChain & LangGraph — Learning Repository

A structured, hands-on course for building LLM-powered applications with LangChain and LangGraph. Each lesson folder contains theory notes and working Python examples that progressively build toward full AI agent systems.

---

## Prerequisites

- Python 3.10+
- A Google Gemini API key (most examples use `langchain-google-genai`)

**Install dependencies:**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Set your API key** (add to your shell profile or a `.env` file):

```bash
export GOOGLE_API_KEY="your-key-here"
```

---

## Repository Structure

```
langGraph/
├── Introduction.md               ← You are here
├── requirements.txt              ← All dependencies
├── Examples/                     ← Standalone end-to-end examples
│   └── documentReader/
│
├── Lesson00-AllAboutGenAI/       ← Core GenAI theory (LLMs, tokens, RAG, evals, memory)
├── Lesson00-MustKnowPython/      ← Python fundamentals needed for this course
│
│   ── LangChain ──
├── Lesson01-Basics/              ← First LangChain call, project setup
├── Lesson02-Prompting/           ← Prompt templates, chat history, chatbot
├── Lesson03-StructuredOutput/    ← Output parsers, Pydantic models
├── Lesson04-ChainsAndRunnables/  ← LCEL chains, Runnables, pipe operator
├── Lesson05-DocumentLoaders/     ← Loading text, PDFs, and other documents
├── Lesson06-TextSplitting/       ← RecursiveCharacterTextSplitter, chunk overlap
├── Lesson07-VectorStore/         ← Chroma, FAISS — storing and searching embeddings
├── Lesson08-Retriever/           ← Simple, MMR, multi-query, compression retrievers
├── Lesson09-Tool/                ← Custom tools, DuckDuckGo, shell tool
├── Lesson10-Agent/               ← ReAct agents, tool-calling agents
├── Lesson10-ProjectLangChain/    ← Capstone project: full LangChain application
│
│   ── LangGraph ──
├── Lesson12-LangGraph/           ← LangGraph concepts: nodes, edges, state
├── Lesson13-SequentialWorkflow/  ← Linear node-to-node graphs
├── Lesson14-ParallelWorkflow/    ← Parallel branches with fan-out / fan-in
├── Lesson15-ConditionalWorkflow/ ← Conditional edges and routing logic
├── Lesson16-IterativeWorkflow/   ← Loops and iterative refinement patterns
├── Lesson18-Persistence/         ← Checkpointing, pause/resume, human-in-the-loop
└── Lesson17-ProjectLangGraph/    ← Capstone project: full LangGraph agent system
```

---

## How to Use This Repo

1. **Start with theory** — Read `Lesson00-AllAboutGenAI/Theory.md` for a complete reference on LLMs, tokens, model params, RAG, evals, and memory.
2. **Brush up on Python** — Work through `Lesson00-MustKnowPython/` if you need a refresher on the Python patterns used throughout.
3. **Follow lessons in order** — Each lesson builds on the previous. Read the `_*.md` theory file inside each folder first, then run the `.py` examples.
4. **Run examples directly** — All scripts are self-contained. From the repo root:
   ```bash
   python Lesson01-Basics/hello_world_langchain.py
   ```
5. **Check the capstone projects** — `Lesson10-ProjectLangChain/` and `Lesson17-ProjectLangGraph/` combine everything into real applications.

---

## Lesson Overview

| Lesson | Topic | Key Concepts |
|--------|-------|--------------|
| 00 | GenAI Theory | LLMs, tokens, model params, RAG, evals, memory |
| 00 | Must-Know Python | Decorators, type hints, Pydantic, async |
| 01 | Basics | LangChain setup, first LLM call |
| 02 | Prompting | PromptTemplate, ChatPromptTemplate, chat history |
| 03 | Structured Output | Pydantic output parsers, JSON responses |
| 04 | Chains & Runnables | LCEL, `\|` pipe, RunnablePassthrough |
| 05 | Document Loaders | TextLoader, PyPDFLoader |
| 06 | Text Splitting | RecursiveCharacterTextSplitter, chunk overlap |
| 07 | Vector Stores | Chroma, FAISS, embedding + storage |
| 08 | Retrievers | Simple, MMR, multi-query, contextual compression |
| 09 | Tools | Custom tools, `@tool` decorator, search, shell |
| 10 | Agents | ReAct loop, tool-calling agents |
| 12 | LangGraph Intro | Graph, StateGraph, nodes, edges, TypedDict state |
| 13 | Sequential Workflow | Linear multi-step graphs |
| 14 | Parallel Workflow | Fan-out, fan-in, parallel node execution |
| 15 | Conditional Workflow | Dynamic routing with conditional edges |
| 16 | Iterative Workflow | Loops, self-refinement, convergence conditions |
| 18 | Persistence | Checkpointers, thread IDs, human-in-the-loop |
| 17 | Project LangGraph | Full stateful agent system |

---

## Tech Stack

| Package | Version | Purpose |
|---------|---------|---------|
| `langchain` | 1.3.2 | Core LangChain framework |
| `langchain-google-genai` | 4.2.4 | Gemini model integration |
| `langgraph` | 1.2.2 | Graph-based agent orchestration |
| `langsmith` | 0.8.7 | Tracing and evaluation |
| `pydantic` | 2.13.4 | Data validation and structured output |
| `google-genai` | 2.7.0 | Google Generative AI SDK |


Note: Instead of google gemini, other models can be used.
