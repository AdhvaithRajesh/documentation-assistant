import os
from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import PineconeEmbeddings, PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List, Dict, Any

INDEX_NAME="langchain-doc-index"

load_dotenv()
GOOGLE_API_KEY = os.environ["GEMINI_API_KEY"]

def run_llm(query:str, chat_history:List[Dict[str,Any]] = []):
    embeddings = PineconeEmbeddings(model="multilingual-e5-large")
    docsearch = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=GOOGLE_API_KEY)

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    stuff_documents_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)

    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

    history_aware_retriever = create_history_aware_retriever(
        llm=llm,
        retriever=docsearch.as_retriever(),
        prompt=rephrase_prompt
    )

    qa = create_retrieval_chain(
        retriever=history_aware_retriever,
        combine_docs_chain=stuff_documents_chain
    )

    result = qa.invoke(input={"input":query, "chat_history":chat_history})
    
    new_result = {
        "query": result["input"],
        "result": result["answer"],
        "source_documents": result["context"]
    }

    return new_result

if __name__ == "__main__":
    res = run_llm(query="What is a Langchain chain?")
    print(res["result"])