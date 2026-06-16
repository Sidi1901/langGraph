### Content





### Document

#### What is Document?
A LangChain document contains:
1. page_content → actual text
2. metadata → information about the source

<pre>
---------------------------------------
Document(                              |
    page_content="This is the text",   |
    metadata={"source": "file.pdf"}    |
)                                      |
---------------------------------------
</pre>


### Document loaders

A document loader in LangChain is a component that ingests data from external sources such as PDFs, websites, databases, CSVs, or text files and converts it into standardized Document objects that can be processed by text splitters, embedding models, and vector stores.

LLMs cannot directly read PDFs, Word files, websites, databases, etc.

Think of it as data ingestion layer of a RAG pipeline.


<pre>

| Loader                           | Reads          |
| -------------------------------- | -------------- |
| `TextLoader`                     | .txt files     |
| `PyPDFLoader`                    | PDF files      |
| `CSVLoader`                      | CSV files      |
| `JSONLoader`                     | JSON files     |
| `WebBaseLoader`                  | Websites       |
| `DirectoryLoader`                | Entire folders |
| `UnstructuredWordDocumentLoader` | Word documents |

For most RAG applications, above document loaders cover 80–90% of use cases

</pre>


#### TextLoader

TextLoader is specifically for reading text files.
In below example, tt reads the contents of notes.txt and creates a Document object.

-----------------------------------------------------------
Example : Text Loader

from langchain_community.document_loaders import TextLoader

loader = TextLoader("notes.txt")
docs = loader.load()

"""
Document(
    page_content="Hello World",
    metadata={"source": "notes.txt"}
)

"""

print(docs[0].page_content)

// Hello World

-------------------------------------------------------



#### PyPDFLoader
Each PDF page becomes a document.

-----------------------------------------------------
Example : PyPdfloader

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("book.pdf")
docs = loader.load()


#### Custom data loader