from dotenv import load_dotenv
import langfuse
load_dotenv()

from graph.workflow import build_graph
from agents.retrieval import scrape_products, fetch_stock_data, fetch_forex_rate
from visualization.charts import plot_prices
from monitoring.langfuse_setup import langfuse

import os

print("PUBLIC:", os.getenv("LANGFUSE_PUBLIC_KEY"))
print("SECRET:", os.getenv("LANGFUSE_SECRET_KEY"))
print("HOST:", os.getenv("LANGFUSE_BASE_URL"))

url = "http://books.toscrape.com/"
raw_products = scrape_products(url)
raw_stocks = fetch_stock_data("AAPL")
raw_forex = fetch_forex_rate("USDINR=X")

graph = build_graph()

# Root span
root_span = langfuse.start_span(name="agent-run")

print("Products:", len(raw_products))
print("Stocks:", len(raw_stocks))
print("Forex:", len(raw_forex))
result = graph.invoke({
    "products": raw_products,
    "stocks": raw_stocks,
    "forex": raw_forex,
    "user_query": "Analyze current stock and forex trends and product prices",
    "langfuse_parent_span": root_span
})

root_span.end()

print("\nFINAL RESULT:\n")
print(result)

# Plot structured products
plot_prices(result.get("structured_products", []))
