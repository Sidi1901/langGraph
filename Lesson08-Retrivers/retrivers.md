### Phase 4 — Retrieval Strategies

#### Similarity Search

The default strategy. Returns the top-k vectors closest to the query vector.

<pre>
+-----------------------------------------------------------------------+
| EXAMPLE: Basic Similarity Search                                      |
|                                                                       |
| results = vector_store.similarity_search(                             |
|     "What is LangChain?",                                             |
|     k=3                       ← return top 3 matches                 |
| )                                                                     |
|                                                                       |
| # Results are Document objects with page_content + metadata           |
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
| EXAMPLE: MMR Search                                                   |
|                                                                       |
| results = vector_store.max_marginal_relevance_search(                 |
|     "How does Kafka work?",                                           |
|     k=4,           ← final results returned                          |
|     fetch_k=20     ← candidate pool ANN searches first               |
| )                                                                     |
|                                                                       |
| Use MMR when you need broad coverage, not just the most similar chunk.|
+-----------------------------------------------------------------------+
</pre>


#### Score Threshold Search

Filter out results below a minimum similarity score.

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
| Prevents low-quality context from entering the LLM prompt.            |
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
