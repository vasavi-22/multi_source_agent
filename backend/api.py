# from fastapi import FastAPI
# from agents.retrieval import scrape_products, fetch_stock_data, fetch_forex_rate
# from graph.workflow import build_graph
# from monitoring.langfuse_setup import langfuse
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()
# graph = build_graph()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.post("/run-agent")
# def run_agent():
#     url = "http://books.toscrape.com/"

#     root_span = langfuse.start_span(name="agent-run-api")

#     try:
#         raw_products = scrape_products(url)
#         stocks = fetch_stock_data("AAPL")
#         forex = fetch_forex_rate("USDINR=X")
        
#         result = graph.invoke({
#             "products": raw_products,
#             "stocks": stocks,
#             "forex": forex,
#             "langfuse_parent_span": root_span
#         })
#         return {
#             "structured_products": result.get("structured_products"),
#             "analysis": result.get("analysis"),
#             "alerts": result.get("decision"),
#             "action": result.get("action")
#         }
#     finally:
#         root_span.end()


from fastapi import FastAPI
from agents.retrieval import (
    scrape_products,
    fetch_stock_data,
    fetch_forex_rate
)
from graph.workflow import build_graph
from monitoring.langfuse_setup import langfuse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
graph = build_graph()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# PRODUCT AGENT
# -----------------------
@app.post("/run-agent")
def run_agent():
    url = "http://books.toscrape.com/"
    root_span = langfuse.start_span(name="product-agent")

    try:
        raw_products = scrape_products(url)

        result = graph.invoke({
            "products": raw_products,
            "langfuse_parent_span": root_span
        })

        return {
            "structured_products": result.get("structured_products"),
            "analysis": result.get("analysis"),
            "alerts": result.get("decision"),
            "action": result.get("action")
        }

    finally:
        root_span.end()


# -----------------------
# FINANCE AGENT
# -----------------------
@app.post("/run-finance-agent")
def run_finance_agent():
    root_span = langfuse.start_span(name="finance-agent")

    try:
        stocks = fetch_stock_data("AAPL")
        forex = fetch_forex_rate("USDINR=X")

        result = graph.invoke({
            "stocks": stocks,
            "forex": forex,
            "langfuse_parent_span": root_span
        })

        return {
            "analysis": result.get("analysis"),
            "alerts": result.get("decision"),
            "action": result.get("action")
        }

    finally:
        root_span.end()