from typing import Any, Dict, List
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone as PineconeLangChain
from pinecone import Pinecone
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
load_dotenv()
Pinecone.api_key = os.environ.get("PINECONE_API_KEY")
pc = Pinecone(
    api_key=os.environ.get("PINECONE_API_KEY")
)

INDEX_NAME = "docs-helper"

def run_llm(query:str, chat_history: List[Dict[str, Any]] = []) -> Any:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    docsearch = PineconeLangChain.from_existing_index(embedding=embeddings, index_name=INDEX_NAME)
    llm = ChatOpenAI(model_name="gpt-4-0125-preview", temperature=0) 
    # qa = RetrievalQA.from_chain_type(
    #     llm, chain_type="stuff", retriever=docsearch.as_retriever(), return_source_documents=True,
    # )
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=docsearch.as_retriever(), return_source_documents=True
    )
    result = qa.invoke({"question": query, "chat_history": chat_history})
    return result

if __name__ == "__main__":
    print(run_llm(query="What is RetrievalQA?"))