from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# def analyze_prices(products):
#     flat_products = [p["product_node"] for p in products]
#     prices = [float(p["price"]) for p in flat_products]
#     cheapest = min(flat_products, key=lambda x: float(x["price"]))
#     avg_price = sum(prices) / len(prices)

#     summary = f"""
#     Cheapest product: {cheapest['title']} at ₹{cheapest['price']}.
#     It is the best deal because it has the lowest price.
#     Average price across products: ₹{avg_price:.2f}.
#     """
#     return {
#         "summary": summary,
#         "products": flat_products
#     }

# def analyze_prices(products):
#     """
#     Uses LLM to analyze structured product data
#     """
#     # Flatten structured products
#     flat_products = [p["product_node"] for p in products]
#     llm = ChatOpenAI(
#         model="gpt-4o-mini",
#         temperature=0
#     )
#     prompt = ChatPromptTemplate.from_template("""
#     You are a price comparison assistant.

#     Here is product price data:
#     {products}

#     Tasks:
#     1. Identify the cheapest product.
#     2. Explain briefly why it is the best deal.
#     3. Mention the average price trend.

#     Keep response concise.
#     """)

#     chain = prompt | llm | StrOutputParser()
#     response = chain.invoke({
#         "products": flat_products
#     })
#     return {
#         "summary": response,
#         "products": flat_products
#     }

def analyze_prices(products, parent_span=None):
    span = parent_span.start_span(name="llm-price-analysis") if parent_span else None
    try:
        flat_products = [p["product_node"] for p in products]
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        prompt = ChatPromptTemplate.from_template("""
        You are a price comparison assistant.
        Product data:
        {products}
        Provide:
        - Cheapest product
        - Average price
        - Short recommendation
        """)

        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({"products": flat_products})
        prices = [p["price"] for p in flat_products]
        avg_price = sum(prices) / len(prices)
        return {
            "summary": response,
            "insights": {
                "average_price": avg_price,
                "min_price": min(prices),
                "max_price": max(prices)
            },
            "raw_data": flat_products
        }

    finally:
        if span:
            span.end()

def analyze_stock_trends(structured_stock_data, parent_span=None):
    span = parent_span.start_span(name="llm-stock-analysis") if parent_span else None
    try:
        flat_data = [s["stock_node"] for s in structured_stock_data]
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        prompt = ChatPromptTemplate.from_template("""
        You are a financial analyst.
        Stock data:
        {data}
        Provide:
        - Overall trend
        - Highest close
        - Lowest close
        - Short insight
        """)

        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({"data": flat_data})
        closes = [s["close"] for s in flat_data]

        return {
            "summary": response,
            "insights": {
                "max_close": max(closes),
                "min_close": min(closes),
            },
            "raw_data": flat_data
        }
    finally:
        if span:
            span.end()


def analyze_forex_trends(structured_forex_data, parent_span=None):
    span = parent_span.start_span(name="llm-forex-analysis") if parent_span else None
    try:
        flat_data = [f["forex_node"] for f in structured_forex_data]
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

        prompt = ChatPromptTemplate.from_template("""
        You are a forex analyst.
        Forex data:
        {data}
        Provide:
        - Rate trend
        - Highest rate
        - Lowest rate
        - Short explanation
        """)
        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({"data": flat_data})

        rates = [f["rate"] for f in flat_data]

        return {
            "summary": response,
            "insights": {
                "max_rate": max(rates),
                "min_rate": min(rates),
            },
            "raw_data": flat_data
        }
    finally:
        if span:
            span.end()
            
def analyze(state):
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    prompt = f"""
    Live Market Data:
    {state["structured_data"]}

    Knowledge Base Context:
    {state.get("rag_context", "")}

    Provide detailed analysis and recommendations.
    """

    response = llm.invoke(prompt)

    state["analysis"] = response.content

    return state