



#### Length based text splitting


#### Text Structure based
    

#### 


https://chunkviz.up.railway.app/


#### Chunking Before Embedding

You cannot embed an entire document as one vector — the embedding model has a
token limit, and one large vector loses local detail. Documents must be split
into chunks first. This is the job of a Text Splitter (covered in Lesson 06).

Chunking strategy directly affects retrieval quality.

| Strategy                  | Description                                    |
|---------------------------|------------------------------------------------|
| Fixed-size (CharacterSplitter) | Split every N characters, with overlap    |
| Recursive                 | Split on paragraphs → sentences → words       |
| Semantic                  | Split where meaning changes (experimental)    |

overlap: Each chunk shares some text with the adjacent chunk so context isn't lost
at boundaries.

<pre>
+-----------------------------------------------------------------------+
| EXAMPLE: Chunking + Embedding Flow                                    |
|                                                                       |
| Document: "LangChain is a framework... [2000 words]"                 |
|                                                                       |
| After splitting (chunk_size=500, overlap=50):                         |
|   Chunk 1: "LangChain is a framework for building LLM apps..."        |
|   Chunk 2: "...LLM apps. It provides chains, agents, and tools..."    |
|   Chunk 3: "...tools and memory to compose complex workflows..."      |
|                                                                       |
| Each chunk → embed → store in vector store independently.             |
+-----------------------------------------------------------------------+
</pre>

