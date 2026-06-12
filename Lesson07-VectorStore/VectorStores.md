
### Content

1. **Embeddings**
   - What is an Embedding
   - Embedding Models
2. **Vector Store Internals**
   - What is a Vector Store
   - What a Vector Store Holds
   - ANN Search
   - Distance / Similarity Metrics
   - Indexing Algorithms
3. **Key Features & Implementations**
   - Key Features
   - FAISS vs Chroma
   - Vector Store vs Vector Database
   - Common Methods
4. **RAG Integration**
   - Full RAG Pipeline

### Phase 1 — Embeddings

#### What is an Embedding

An embedding is a numerical representation of data that captures its semantic meaning.

Embedding = Text (or Image, Audio…) → Fixed-length array of numbers

The key property: **semantically similar inputs produce numerically similar vectors.**

<pre>
+-----------------------------------------------------------------------+
| EXAMPLE: Semantic Similarity in Vector Space                          |
|                                                                       |
| "dog"  → [0.21, -0.54, 0.87, ...]    ─┐                               |
| "puppy"→ [0.19, -0.51, 0.84, ...]    ─┤  Close together               |
| "car"  → [-0.72, 0.33, -0.10, ...]   ─┘  Far away                     |
|                                                                       |
| "dog" and "puppy" are semantically similar → their vectors are        |
| numerically close. "car" is unrelated → far away in vector space.     |
+-----------------------------------------------------------------------+
</pre>

The number of dimensions in a vector is set by the embedding model.
A common size is 1536 dimensions (OpenAI text-embedding-3-small).


#### Embedding Models

The embedding model converts text into vectors. You must use the **same model** at
indexing time and query time, or comparisons are meaningless.

Example: text-embedding-3-small, gemini-embedding-001

Common embedding models:

| Model                            | Provider    | Dimensions |
|----------------------------------|-------------|------------|
| text-embedding-3-small           | OpenAI      | 1536       |
| text-embedding-3-large           | OpenAI      | 3072       |
| gemini-embedding-001             | Google      | 3072       |
| all-MiniLM-L6-v2                 | HuggingFace | 384        |

Note: Local HuggingFace models (like all-MiniLM-L6-v2) are free and run offline,
but produce lower-quality embeddings than hosted models.


### Phase 2 — Vector Store Internals

#### What is a Vector Store
A vector store is a specialized storage system that saves embeddings (vectors) alongside their original content, and lets you search them by semantic similarity rather than exact keyword match.

#### What a Vector Store Holds

A vector store doesn't just hold a long array of numbers. It binds three things together:

- **ID** — A unique identifier for each record.
- **Vector** — The mathematical representation (e.g., a 1536-dimensional array).
- **Payload / Metadata** — The original text, a URL, a file path, tags (author, date, source), etc.


#### ANN Search

Vector stores don't do exact search — they do **Approximate Nearest Neighbor (ANN) search**.

Approximate Nearest Neighbor (ANN) is an algorithm strategy for finding vectors that are close enough to a query vector — trading a small amount of accuracy for a massive speed gain.


***The problem it solves***
In a vector database, you embed data as high-dimensional vectors (e.g., 1536 dimensions for OpenAI embeddings). Finding the exact nearest neighbor requires comparing your query against every vector in the database — this is exact/brute-force search, which becomes too slow at scale (millions of vectors).

***How ANN works***
Instead of scanning everything, ANN builds an index that partitions or organizes the vector space so you can quickly narrow down candidates, then only compare against those.

***Common ANN index types***
HNSW (Hierarchical Navigable Small World)
IVF (Inverted File Index)	
LSH (Locality-Sensitive Hashing)
ANNOY

In vector stores like Chroma, FAISS, Pinecone, and Weaviate all use ANN indexes internally. When you do a similarity search, you're using ANN — you get fast, good enough results rather than slow, perfect ones.



#### Distance / Similarity Metrics

The "closeness" between two vectors is measured by a metric. The choice affects quality.

| Metric              | Description                                    | Best For             |
|---------------------|------------------------------------------------|----------------------|
| Cosine Similarity   | Angle between vectors (ignores magnitude)      | Text / NLP (default) |
| Dot Product         | Magnitude + angle combined                     | Normalized vectors   |
| Euclidean (L2)      | Straight-line distance                         | Low-dimensional data |

Cosine similarity is the standard for text embeddings.

<pre>
+-----------------------------------------------------------------------+
| EXAMPLE: Cosine Similarity Intuition                                  |
|                                                                       |
| Score = 1.0  → Identical meaning                                      |
| Score = 0.85 → Highly similar (good retrieval result)                 |
| Score = 0.50 → Loosely related                                        |
| Score = 0.0  → Completely unrelated                                   |
| Score < 0    → Opposite meaning (rare in practice)                    |
+-----------------------------------------------------------------------+
</pre>


#### Indexing Algorithms

Indexing is the data structure that makes ANN search fast on millions of vectors.

**HNSW** (Hierarchical Navigable Small World) — Used by FAISS and Chroma.
Builds a multi-layer graph. Fast query time, high memory usage.

**IVF** (Inverted File Index) — Used by FAISS.
Clusters vectors into groups. Lower memory, slightly slower than HNSW.

You rarely configure these directly in LangChain — the library handles it.


### Phase 3 — Key Features & Implementations

#### Key Features

**Storage** : Retains vectors and their payloads, either in-memory or on-disk.

**Similarity Search** : Retrieves the vectors most similar to a query vector.

**Indexing** : Data structure (HNSW, IVF) that makes similarity search fast at scale.

**CRUD Operations** : Add, update, delete vectors by ID.

**Metadata Filtering** : Filter results by payload fields before or after ANN search.

Common Vector Stores: FAISS, Chroma, Pinecone, Weaviate, Qdrant, pgvector


#### FAISS vs Chroma

Both work almost identically from the LangChain perspective.

| Feature             | FAISS                          | Chroma                         |
|---------------------|--------------------------------|--------------------------------|
| Storage             | In-memory (RAM) by default     | On-disk (persisted) by default |
| Metadata support    | Limited                        | Full metadata + filtering      |
| Persistence         | Manual save/load               | Automatic via persist_directory|
| Best for            | Speed, prototyping             | Production, long-term storage  |
| Type                | Vector Indexing Library        | Vector Database                |

Note: FAISS is technically a vector indexing library, not a full database.



#### Vector Store vs Vector Database

Vector database — fully featured database (CRUD, auth, horizontal scaling, cloud-hosted).
Examples: Pinecone, Weaviate, Qdrant.

Vector store — lightweight library or service focused on storing and searching vectors.
Examples: FAISS, Chroma (local).

Both terms are used interchangeably in practice.


#### Common Methods

from_documents -> Create vector store from documents 
add_documents(docs) -> Add more documents to existing store
similarity_search -> Retrieve top-k similar documents 
similarity_search_with_score -> Retrieve with cosine similarity score
max_marginal_relevance_search -> Retrieve with diversity (MMR)   
delete ->  Delete documents by ID 
as_retriever -> Convert store to a LangChain retriever
persist_directory -> Path to save Chroma vectors to disk

Note: Most RAG applications use `as_retriever()` instead of calling
similarity_search() directly.



#### Metadata Filtering

You can filter search results by metadata fields before or after the ANN search.
This is critical for multi-tenant applications or scoped queries.

<pre>
+-----------------------------------------------------------------------+
| EXAMPLE: Chroma Metadata Filter                                       |
|                                                                       |
| results = vector_store.similarity_search(                             |
|     "deployment issues",                                              |
|     k=4,                                                              |
|     filter={"author": "sidi", "date": "2026-06"}                      |
| )                                                                     |
|                                                                       |
| Only returns documents matching both metadata conditions.             |
+-----------------------------------------------------------------------+
</pre>


### Phase 4 — RAG Integration

#### Full RAG Pipeline

RAG (Retrieval-Augmented Generation) is the primary use case for vector stores.
Instead of the LLM answering from training data alone, it answers from retrieved context.

<pre>
+-----------------------------------------------------------------------+
| RAG Pipeline End-to-End                                               |
|                                                                       |
|  INDEXING PHASE (done once, offline)                                  |
|  Raw Documents                                                        |
|       ↓                                                               |
|  Document Loader   ← load PDF, web page, markdown, etc.               |
|       ↓                                                               |
|  Text Splitter     ← split into chunks (see note below)               |
|       ↓                                                               |
|  Embedding Model   ← convert each chunk to a vector                   |
|       ↓                                                               |
|  Vector Store      ← store vector + metadata                          |
|                                                                       |
|  QUERY PHASE (done per user request, online)                          |
|  User Question                                                        |
|       ↓                                                               |
|  Embed Question → Query Vector                                        |
|       ↓                                                               |
|  ANN Search in Vector Store                                           |
|       ↓                                                               |
|  Retrieved Chunks (context)                                           |
|       ↓                                                               |
|  LLM (question + context)                                             |
|       ↓                                                               |
|  Answer                                                               |
+-----------------------------------------------------------------------+
</pre>


