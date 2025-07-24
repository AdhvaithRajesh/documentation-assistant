from dotenv import load_dotenv

load_dotenv()

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_pinecone import PineconeVectorStore
from langchain_pinecone import PineconeEmbeddings
from langchain_openai import OpenAIEmbeddings

# embeddings = PineconeEmbeddings(model="multilingual-e5-large")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small", chunk_size=50
)

def chunks_generator(chunks, size):
    for i in range(0, len(chunks), size):
        yield chunks[i: i+size]

def ingest_docs():
    # loader = ReadTheDocsLoader(r"C:\Personal\Work\documentation-helper\langchain-docs\api.python.langchain.com\en\latest",encoding="utf-8")
    loader = ReadTheDocsLoader(r"langchain-docs\api.python.langchain.com\en\latest", encoding="utf-8")
    
    raw_documents = loader.load()
    print(f"loaded {len(raw_documents)} documents")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=480, chunk_overlap=60)
    documents = text_splitter.split_documents(raw_documents)
    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace('\\','/')
        new_url = new_url.replace(r"langchain-docs/","https://")
        doc.metadata.update({"source": new_url})

    for chunk in chunks_generator(chunks=documents, size=200):
        print(f"{len(chunk)} chunk is being upserted to vector store")
        PineconeVectorStore.from_documents(documents=chunk, embedding=embeddings, index_name="langchain-doc-index") 

    # print(f"Going to add {len(documents)} to Pinecone")
    # PineconeVectorStore.from_documents(
    #     documents, embeddings, index_name="langchain-doc-index",
    #     batch_size = 16
    # )

    print("*** loaded to vectorstore ***")


if __name__ == "__main__":
    ingest_docs()