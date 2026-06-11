from langchain_community.document_loaders import (
    TextLoader,
    WebBaseLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .vector_store import get_vector_store
from langchain_core.documents import Document
import os


def ingest_documents():

    # Get current file directory (rag/)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Build absolute path to docs folder
    docs_path = os.path.join(current_dir, "docs")
    all_docs = []

    # 1️⃣ Load Local Strategy Files
    for file in os.listdir(docs_path):
        if file.endswith(".txt"):
            loader = TextLoader(os.path.join(docs_path, file))
            docs = loader.load()

            # Add metadata (IMPORTANT for filtering)
            for d in docs:
                d.metadata["source_type"] = file.replace(".txt", "")

            all_docs.extend(docs)

    # 2️⃣ Load Investopedia Articles (Real Documents)
    investopedia_urls = [
        "https://www.investopedia.com/terms/r/rsi.asp",
        "https://www.investopedia.com/terms/m/movingaverage.asp",
        "https://www.investopedia.com/terms/p/price-earningsratio.asp",
        "https://www.investopedia.com/terms/f/forex.asp"
    ]

    for url in investopedia_urls:
        loader = WebBaseLoader(url)
        docs = loader.load()

        for d in docs:
            d.metadata["source_type"] = "investopedia"

        all_docs.extend(docs)

    # 3️⃣ Split Documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    split_docs = splitter.split_documents(all_docs)

    # 4️⃣ Store in Pinecone
    vector_store = get_vector_store()
    vector_store.add_documents(split_docs)

    print("✅ Documents successfully stored in Pinecone.")


if __name__ == "__main__":
    ingest_documents()