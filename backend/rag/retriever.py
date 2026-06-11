from .vector_store import get_vector_store

def retrieve_context(query, domain=None):

    vector_store = get_vector_store()
    search_kwargs = {"k": 4}

    # Optional domain filtering
    if domain:
        search_kwargs["filter"] = {
            "source_type": domain
        }
    
    if not query:
        return []

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs=search_kwargs
    )

    # docs = retriever.get_relevant_documents(query)
    docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in docs])

# print(retrieve_context("How to analyze stock trends?", "stock_analysis_guide"))