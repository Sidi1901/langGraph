
### Content

1. **Retriever Fundamentals**
   - What is a Retriever
   - Types of Retrievers
2. **Search Based Retrievers**
   - Similarity Search
   - Similarity Search with Score
   - Score Threshold Search
   - MMR — Maximal Marginal Relevance
   - Multi-Query Retriever
   - Contextual Compression Retriever
3. **Data Source Based Retrievers**
   - Vector Retriever
   - Wikipedia Retriever


### Phase 1 — Retriever

#### What is a Retriever
A Retriever is a component that finds the most relevant documents/chunks for a user's query.
Retrievers are the heart of RAG systems. Poor retrieval usually causes poor answers even when the LLM is excellent.

***Why use retrievers instead of vector store search directly?***

Vector store `.similarity_search()` always uses cosine similarity. Retrievers expose a unified `.get_relevant_documents()` interface and accept a `search_type` parameter — so you can swap in MMR, threshold filtering, or multi-query without changing any downstream code.

#### Types of Retrievers

**Search based**

1. Similarity Search
2. Similarity Search with Score
3. Score Threshold Search
4. MMR Retriever
5. Multi-Query Retriever
6. Contextual Compression Retriever

**Data source based**

1. Vector Retriever
2. Wikipedia Retriever, etc


### Phase 2 — Search Based Retrievers

#### Similarity Search

The default strategy. Returns the top-k vectors closest to the query vector using cosine similarity.

<pre>
+-----------------------------------------------------------------------+
| EXAMPLE: Basic Similarity Search                                      |
|                                                                       |
| retriever = vector_store.as_retriever(                                |
|     search_type="similarity",                                         |
|     search_kwargs={"k": 3}                                            |
| )                                                                     |
|                                                                       |
| docs = retriever.get_relevant_documents("What is LangChain?")         |
|                                                                       |
| # Returns top 3 Document objects with page_content + metadata         |
+-----------------------------------------------------------------------+
</pre>


#### Similarity Search with Score

Same as similarity search but also returns the similarity score alongside each document.
Useful when you want to inspect or log how confident the retrieval was.

<pre>
+-----------------------------------------------------------------------+
| EXAMPLE: Similarity Search with Score                                 |
|                                                                       |
| results = vector_store.similarity_search_with_score(                  |
|     "What is LangChain?",                                             |
|     k=3                                                               |
| )                                                                     |
|                                                                       |
| for doc, score in results:                                            |
|     print(f"Score: {score:.4f} | {doc.page_content[:60]}")            |
|                                                                       |
| # Score is cosine similarity — higher means more relevant.            |
| # Score: 0.9121 | LangChain is a framework for building LLM apps...   |
+-----------------------------------------------------------------------+
</pre>


#### Score Threshold Search

Filter out results below a minimum similarity score.
Prevents low-quality or unrelated chunks from entering the LLM prompt.

<pre>
+-----------------------------------------------------------------------+
| EXAMPLE: Threshold-Based Retrieval                                    |
|                                                                       |
| retriever = vector_store.as_retriever(                                |
|     search_type="similarity_score_threshold",                         |
|     search_kwargs={"score_threshold": 0.75}                           |
| )                                                                     |
|                                                                       |
| Only returns documents with cosine similarity >= 0.75.                |
| If no document clears the threshold, returns an empty list.           |
+-----------------------------------------------------------------------+
</pre>


#### MMR — Maximal Marginal Relevance

A standard similarity search returns the top-N most similar documents, but these often end up being near-duplicates of each other — you get lots of redundant information and miss coverage of different aspects of your query.

Maximal Marginal Relevance (MMR) is a retrieval algorithm that balances two competing goals when selecting documents:

Relevance — how similar a document is to the query
Diversity — how different a document is from already-selected documents

<pre>
+-----------------------------------------------------------------------------------+
| EXAMPLE: MMR Retriever                                                            |
|                                                                                   |
| Documents in Vector Store:                                                        |
|                                                                                   |
| D1 : Climate change is causing glaciers to melt rapidly in the arctic region.     |
| D2 : Glaciers in the arctic are melting at an alarming rate due to rising temp.   |
| D3 : Deforestation in the Amazon is accelerating global climate change.           |
| D4 : Climate change is increasing the frequency of wildfires in California.       |
| D5 : Rising sea levels due to climate change threaten coastal cities.             |
| D6 : Deforestation in the Amazon is accelerating global climate change.           |
+-----------------------------------------------------------------------------------+
| Query: "climate change effects"                                                   |
+-----------------------------------------------------------------------------------+
| Similarity Search (k=3) — top-3 most similar, but redundant:                      |
|   D1 : Climate change is causing glaciers to melt rapidly in the arctic region.   |
|   D2 : Glaciers in the arctic are melting at an alarming rate due to rising temp. |
|   D3 : Deforestation in the Amazon is accelerating global climate change.         |
+-----------------------------------------------------------------------------------+
| MMR Search (k=3) — relevant AND diverse:                                          |
|   D1 : Climate change is causing glaciers to melt rapidly in the arctic region.   |
|   D4 : Climate change is increasing the frequency of wildfires in California.     |
|   D5 : Rising sea levels due to climate change threaten coastal cities.           |
+-----------------------------------------------------------------------------------+
| Result: MMR avoids near-duplicate D2 and picks D4, D5 for better coverage.        |
+-----------------------------------------------------------------------------------+
</pre>


#### Multi-Query Retriever

Problem: A user's single query may not match the wording of stored documents well.

The Multi-Query Retriever uses an LLM to generate multiple rephrased variants of the
original query, runs all of them, then merges the unique results.

***How it Works***
Query Expansion: The LLM takes the initial prompt and generates (by default) 3 alternative versions.

Bulk Retrieval: LangChain runs a similarity search for all variations against your vector database.

Deduplication: It combines all the resulting documents and removes duplicates, ensuring a richer, more comprehensive set of context for your final answer.

Original Query
    ↓
LLM generates variants:
  - Variant 1 → search → docs
  - Variant 2 → search → docs
  - Variant 3 → search → docs
    ↓
Merge unique results
    ↓
Final context for LLM

This increases recall at the cost of extra LLM calls.

<pre>
+-----------------------------------------------------------------------------------+
| EXAMPLE: Multi-Query Retriever                                                    |
|                                                                                   |
| WHY IT MATTERS — The Vocabulary Mismatch Problem:                                 |
|                                                                                   |
|   Documents use:  "Kafka broker latency", "consumer lag", "throughput bottleneck" |
|   User types:     "Why is my Kafka slow?"                                         |
|                                                                                   |
|   A plain vector search on "Why is my Kafka slow?" may miss documents that        |
|   use technical terms like "latency" or "throughput" because the embeddings       |
|   of informal phrasing sit far from formal documentation in vector space.         |
+-----------------------------------------------------------------------------------+
| STEP 1 — LLM generates query variants from the original:                          |
|                                                                                   |
|   Original : "Why is my Kafka slow?"                                              |
|   Variant 1: "Kafka performance degradation causes"                               |
|   Variant 2: "Kafka broker throughput issues"                                     |
|   Variant 3: "How to improve Kafka consumer speed"                                |
+-----------------------------------------------------------------------------------+
| STEP 2 — Each variant runs a separate vector search:                              |
|                                                                                   |
|   "Why is my Kafka slow?"              → [D1, D2, D3]                             |
|   "Kafka performance degradation"      → [D2, D4, D5]                             |
|   "Kafka broker throughput issues"     → [D3, D5, D6]                             |
|   "How to improve Kafka consumer speed"→ [D1, D6, D7]                             |
+-----------------------------------------------------------------------------------+
| STEP 3 — Deduplicate and merge all results:                                       |
|                                                                                   |
|   Union: {D1, D2, D3, D4, D5, D6, D7}                                             |
|   Duplicates removed → 7 unique docs instead of the original 3                    |
+-----------------------------------------------------------------------------------+
| RESULT — Better recall, wider coverage:                                           |
|                                                                                   |
|   Without Multi-Query: only docs matching "slow" phrasing are found.              |
|   With Multi-Query:    docs using "latency", "throughput", "consumer lag"         |
|                        are all retrieved, giving the LLM richer context.          |
|                                                                                   |
|   Trade-off: 4 LLM calls (1 original + 3 variants) instead of 1.                  |
+-----------------------------------------------------------------------------------+
</pre>


#### Contextual Compression Retriever

Problem: Retrieved chunks often contain irrelevant sentences padded around the useful part.
Sending noisy chunks to the LLM wastes tokens and degrades answer quality.

The Contextual Compression Retriever wraps another retriever and passes each retrieved
document through a compressor (usually an LLM) that extracts only the relevant portion.

Original Retriever
    ↓
Fetch candidate docs
    ↓
Compressor (LLM extracts relevant sentences)
    ↓
Compressed, focused chunks
    ↓
LLM prompt

<pre>
+-----------------------------------------------------------------------------------+
| EXAMPLE: Contextual Compression Retriever                                         |
|                                                                                   |
| WHY IT MATTERS — The Noisy Chunk Problem:                                         |
|                                                                                   |
|   When text is split into chunks for embedding, each chunk is a fixed-size        |
|   window of text. A chunk matched by vector search might be mostly about          |
|   something else, with only 1-2 relevant sentences buried inside it.             |
|                                                                                   |
|   Passing that whole noisy chunk to the LLM wastes tokens and can confuse it.    |
+-----------------------------------------------------------------------------------+
| Query: "What causes OOMKilled in Kubernetes?"                                     |
+-----------------------------------------------------------------------------------+
| STEP 1 — Base retriever fetches 5 full chunks from the vector store:              |
|                                                                                   |
|   Chunk 1 (full, ~200 words):                                                     |
|     "Kubernetes schedules pods onto nodes based on resource requests...           |
|      Pods can be OOMKilled when they exceed their memory limit. This              |
|      happens when the container uses more RAM than specified in the               |
|      resources.limits.memory field. Kubernetes also supports horizontal           |
|      pod autoscaling based on CPU metrics. You can configure liveness             |
|      probes to restart unhealthy containers..."                                   |
+-----------------------------------------------------------------------------------+
| STEP 2 — LLM compressor reads each chunk and extracts only relevant sentences:   |
|                                                                                   |
|   Compressed Chunk 1 (~20 words):                                                 |
|     "Pods can be OOMKilled when they exceed their memory limit, set in            |
|      resources.limits.memory."                                                    |
|                                                                                   |
|   (Sentences about autoscaling, probes, scheduling → discarded as irrelevant)    |
+-----------------------------------------------------------------------------------+
| STEP 3 — Only the compressed, focused sentences reach the LLM prompt:            |
|                                                                                   |
|   Without compression : 5 chunks × ~200 words = ~1000 words sent to LLM         |
|   With compression    : 5 chunks × ~20 words  = ~100 words sent to LLM          |
|                                                                                   |
|   10x fewer tokens, no irrelevant noise, better and cheaper LLM answers.         |
+-----------------------------------------------------------------------------------+
| Trade-off: Each retrieved chunk requires an extra LLM call to compress it.        |
|   5 docs fetched → 5 compression calls + 1 final answer call = 6 LLM calls.      |
+-----------------------------------------------------------------------------------+
</pre>


### Phase 3 — Data Source Based Retrievers

#### Vector Retriever

The Vector Retriever is the standard retriever backed by a vector store.
It converts the query into an embedding and searches the vector index.

This is the most common retriever in RAG pipelines.

<pre>
+-----------------------------------------------------------------------+
| EXAMPLE: Vector Retriever via as_retriever()                          |
|                                                                       |
| from langchain_chroma import Chroma                                   |
| from langchain_openai import OpenAIEmbeddings                         |
|                                                                       |
| vector_store = Chroma(                                                |
|     collection_name="docs",                                           |
|     embedding_function=OpenAIEmbeddings()                             |
| )                                                                     |
|                                                                       |
| retriever = vector_store.as_retriever(search_kwargs={"k": 4})         |
|                                                                       |
| # The retriever embeds the query at runtime and searches the index.   |
| docs = retriever.get_relevant_documents("What is LangGraph?")         |
+-----------------------------------------------------------------------+
</pre>


#### Wikipedia Retriever

The Wikipedia Retriever fetches live Wikipedia articles as context documents.
No vector store or embedding is needed — it queries the Wikipedia API directly.

Useful when:
- You need up-to-date factual knowledge not in your private corpus.
- You want to ground answers in a publicly verifiable source.

***There are other source based retrievers as well.***