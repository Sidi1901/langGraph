
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
|     print(f"Score: {score:.4f} | {doc.page_content[:60]}")           |
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

Problem with pure similarity search: the top-k results are often near-duplicates,
providing redundant information.

MMR balances relevance and diversity.

For each result:
- It must be similar to the query (relevance).
- It must be different from already-selected results (diversity).

<pre>
+-----------------------------------------------------------------------+
| EXAMPLE: MMR Retriever                                                |
|                                                                       |
| retriever = vector_store.as_retriever(                                |
|     search_type="mmr",                                                |
|     search_kwargs={"k": 4, "fetch_k": 20}                            |
| )                                                                     |
|                                                                       |
| # fetch_k=20  ← candidate pool ANN fetches first                     |
| # k=4         ← final diverse results returned from the pool          |
|                                                                       |
| Use MMR when you need broad coverage, not just the most similar chunk.|
+-----------------------------------------------------------------------+
</pre>


#### Multi-Query Retriever

Problem: A user's single query may not match the wording of stored documents well.

The Multi-Query Retriever uses an LLM to generate multiple rephrased variants of the
original query, runs all of them, then merges the unique results.

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
+-----------------------------------------------------------------------+
| EXAMPLE: Multi-Query Retriever                                        |
|                                                                       |
| from langchain.retrievers import MultiQueryRetriever                  |
|                                                                       |
| retriever = MultiQueryRetriever.from_llm(                             |
|     retriever=vector_store.as_retriever(),                            |
|     llm=llm                                                           |
| )                                                                     |
|                                                                       |
| User query: "Why is my Kafka slow?"                                   |
| Generated variants:                                                   |
|   - "Kafka performance degradation causes"                            |
|   - "Kafka broker throughput issues"                                  |
|   - "How to improve Kafka consumer speed"                             |
+-----------------------------------------------------------------------+
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
+-----------------------------------------------------------------------+
| EXAMPLE: Contextual Compression Retriever                             |
|                                                                       |
| from langchain.retrievers import ContextualCompressionRetriever       |
| from langchain.retrievers.document_compressors import LLMChainExtractor|
|                                                                       |
| base_retriever = vector_store.as_retriever(search_kwargs={"k": 5})   |
|                                                                       |
| compressor = LLMChainExtractor.from_llm(llm)                          |
|                                                                       |
| retriever = ContextualCompressionRetriever(                           |
|     base_compressor=compressor,                                       |
|     base_retriever=base_retriever                                     |
| )                                                                     |
|                                                                       |
| docs = retriever.get_relevant_documents("What causes OOMKilled?")     |
|                                                                       |
| # Each doc is trimmed to only the sentences relevant to the query.    |
+-----------------------------------------------------------------------+
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
| retriever = vector_store.as_retriever(search_kwargs={"k": 4})        |
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

<pre>
+-----------------------------------------------------------------------+
| EXAMPLE: Wikipedia Retriever                                          |
|                                                                       |
| from langchain_community.retrievers import WikipediaRetriever         |
|                                                                       |
| retriever = WikipediaRetriever(                                        |
|     top_k_results=2,      ← number of Wikipedia articles to fetch    |
|     doc_content_chars_max=1000  ← truncate each article at 1000 chars |
| )                                                                     |
|                                                                       |
| docs = retriever.get_relevant_documents("Kafka distributed systems")  |
|                                                                       |
| # Returns Document objects with Wikipedia content as page_content     |
| # and article title + URL in metadata.                                |
+-----------------------------------------------------------------------+
</pre>
