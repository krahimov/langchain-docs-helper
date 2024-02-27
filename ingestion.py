from dotenv import load_dotenv



import os

from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Pinecone as PineconeLangChain
from pinecone import Pinecone
import openai
load_dotenv()
Pinecone.api_key = os.environ.get("PINECONE_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
print(os.environ.get("PINECONE_API_KEY"))
pc = Pinecone(
    api_key=os.environ.get("PINECONE_API_KEY"),
)

INDEX_NAME = "docs-helper"


def ingest_docs():
    loader = ReadTheDocsLoader(
        "langchain-docs/api.python.langchain.com/en/latest/chains"
    )

    raw_documents = loader.load()
    print(f"loaded {len(raw_documents)} documents")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    documents = text_splitter.split_documents(raw_documents)
    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})

    embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")
    print(f"Going to add {len(documents)} to Pinecone")
    PineconeLangChain.from_documents(documents, embeddings, index_name=INDEX_NAME)
 
    


if __name__ == "__main__":
    ingest_docs()





   # index = pc.Index(INDEX_NAME)
    # docs = documents
    # embedding_list = []
    # for i in range(0, len(docs)):
    #     embedding_list.append(embeddings.embed_query(docs[i].page_content))

    # for i in range(0, len(docs)):
    #     index.upsert(
    #         vectors=[
    #         {"id": f"vec{i+1}",
    #         "values": embedding_list[i],
    #         "metadata": {"text": docs[i].page_content, 'docIndex': i}
    #         }
    #         ],
    #         namespace=INDEX_NAME
    #     )