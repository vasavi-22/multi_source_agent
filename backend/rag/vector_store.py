import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from .embeddings import get_embeddings

load_dotenv()

def get_vector_store():
    # print("PINECONE_API_KEY:", os.getenv("PINECONE_API_KEY"))

    api_key = os.getenv("PINECONE_API_KEY")
    index_name = "multi-source-knowledge"

    pc = Pinecone(api_key=api_key)

    # Create index if not exists
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            # dimension=1536,  # must match embedding model
            # dimension=1024,  # must match embedding model
            dimension=384,  # must match embedding model
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

    return PineconeVectorStore(
        index_name=index_name,
        embedding=get_embeddings()
    )