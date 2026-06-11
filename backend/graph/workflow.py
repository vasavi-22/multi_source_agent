from typing import Optional, TypedDict, List, Dict
from unittest import result
from langgraph.graph import StateGraph
from agents.processing import ( structure_products_data, structure_stock_data, structure_forex_data )
from agents.analysis import ( analyze_prices, analyze_stock_trends, analyze_forex_trends )
from agents.decision import ( check_price_threshold, check_stock_threshold, check_forex_threshold )
from agents.action import trigger_alerts
from agents.retrieval import knowledge_retrieval
from monitoring.langfuse_setup import langfuse
from datetime import datetime


# STATE
class AgentState(TypedDict, total=False):
    products: List[Dict]
    stocks: List[Dict]
    forex: List[Dict]

    structured_products: List[Dict]
    structured_stocks: List[Dict]
    structured_forex: List[Dict]

    analysis: Optional[Dict]
    decision: Optional[List[Dict]]
    action: Optional[str]
    
    langfuse_parent_span: Optional[object]


# PROCESSING NODE
def processing_node(state: AgentState) -> AgentState:
    parent = state.get("langfuse_parent_span")
    span = parent.start_span(name="processing") if parent else None
    try:
        updates = {}
        
        # STEP 1: Detect Query Domain
        query = state.get("user_query", "").lower()

        if "stock" in query or "market" in query:
            updates["data_type"] = "stock_analysis_guide"
        elif "forex" in query or "currency" in query:
            updates["data_type"] = "forex_strategy"
        elif "product" in query or "price" in query:
            updates["data_type"] = "product_pricing_rules"
        elif "trading" in query:
            updates["data_type"] = "trading_rules"
        else:
            updates["data_type"] = None
            
        # STEP 2: Structure Data
        if state.get("products"):
            updates["structured_products"] = structure_products_data(
                state.get("products", [])
            )
        if state.get("stocks"):
            updates["structured_stocks"] = structure_stock_data(
                state.get("stocks", [])
            )
        if state.get("forex"):
            updates["structured_forex"] = structure_forex_data(
                state.get("forex", [])
            )
        updates["langfuse_parent_span"] = parent
        
        print("\n[PROCESSING NODE OUTPUT]")
        print("Detected Domain:", updates.get("data_type"))
        print("Structured Products:", updates.get("structured_products"))
        print("Structured Stocks:", updates.get("structured_stocks"))
        print("Structured Forex:", updates.get("structured_forex"))
        return updates
    
    finally:
        if span:
            span.end()

# ANALYSIS NODE (LLM)
# def analysis_node(state: ProductsState) -> ProductsState:
#     structured_products = state.get("structured_products", [])
#     if not structured_products:
#         return {"analysis": "No products available for analysis."}

#     analysis_result = analyze_prices(structured_products)

#     return {
#         "analysis": analysis_result
#     }
def analysis_node(state: AgentState) -> AgentState:
    parent = state.get("langfuse_parent_span")
    span = parent.start_span(name="analysis") if parent else None

    try:
        result = {}
        if state.get("structured_products"):
            result["products"] = analyze_prices(
                state["structured_products"],
                parent_span=span
            )
        if state.get("structured_stocks"):
            result["stocks"] = analyze_stock_trends(
                state["structured_stocks"],
                parent_span=span
            )
        if state.get("structured_forex"):
            result["forex"] = analyze_forex_trends(
                state["structured_forex"],
                parent_span=span
            )
        print("\n[ANALYSIS NODE OUTPUT]")
        print(result)
        return {
            "analysis": result,
            "langfuse_parent_span": parent
        }
    finally:
        if span:
            span.end()

# DECISION NODE
# def decision_node(state: AgentState) -> AgentState:
#     parent = state.get("langfuse_parent_span")
#     span = parent.start_span(name="decision") if parent else None
#     try:
#         alerts = []

#         if state.get("structured_products"):
#             alerts.extend(
#                 check_price_threshold(state["structured_products"], 30.0)
#             )
#         if state.get("structured_stocks"):
#             alerts.extend(
#                 check_stock_threshold(state["structured_stocks"], 200)
#             )
#         if state.get("structured_forex"):
#             alerts.extend(
#                 check_forex_threshold(state["structured_forex"], 85)
#             )

#         severity = "low"
#         if len(alerts) > 5:
#             severity = "high"
#         elif len(alerts) > 2:
#             severity = "medium"

#         decision_result = {
#             "alerts": alerts,
#             "count": len(alerts),
#             "severity": severity,
#             "summary": f"{len(alerts)} alerts triggered"
#         }
#         return {
#             "decision": decision_result,
#             "langfuse_parent_span": parent
#         }
#     finally:
#         if span:
#             span.end()

def decision_node(state: AgentState) -> AgentState:
    parent = state.get("langfuse_parent_span")
    span = parent.start_span(name="decision") if parent else None

    try:
        events = []
        analysis = state.get("analysis", {})

        # -------------------
        # PRODUCT DECISIONS
        # -------------------
        if state.get("structured_products"):
            avg_price = (
                analysis.get("products", {})
                .get("insights", {})
                .get("average_price")
            )

            for item in state["structured_products"]:
                node = item["product_node"]
                price = node["price"]

                if price < 30.0:
                    events.append({
                        "type": "product_price_threshold",
                        "domain": "product",
                        "entity": node["name"],
                        "value": price,
                        "threshold": 30.0,
                        "reason": "Price below static threshold"
                    })

                elif avg_price and price < avg_price * 0.7:
                    events.append({
                        "type": "product_discount_anomaly",
                        "domain": "product",
                        "entity": node["name"],
                        "value": price,
                        "reference": avg_price,
                        "reason": "Price significantly below market average"
                    })

        # -------------------
        # STOCK DECISIONS
        # -------------------
        if state.get("structured_stocks"):
            max_close = (
                analysis.get("stocks", {})
                .get("insights", {})
                .get("max_close")
            )

            for item in state["structured_stocks"]:
                node = item["stock_node"]
                close = node["close"]

                if close > 200:
                    events.append({
                        "type": "stock_price_breakout",
                        "domain": "stock",
                        "entity": node["symbol"],
                        "value": close,
                        "threshold": 200,
                        "reason": "Close above breakout threshold"
                    })

                elif max_close and close == max_close:
                    events.append({
                        "type": "stock_new_high",
                        "domain": "stock",
                        "entity": node["symbol"],
                        "value": close,
                        "reason": "New recent high detected"
                    })

        # -------------------
        # FOREX DECISIONS
        # -------------------
        if state.get("structured_forex"):
            max_rate = (
                analysis.get("forex", {})
                .get("insights", {})
                .get("max_rate")
            )

            for item in state["structured_forex"]:
                node = item["forex_node"]
                rate = node["rate"]

                if rate > 85:
                    events.append({
                        "type": "forex_rate_spike",
                        "domain": "forex",
                        "entity": node["pair"],
                        "value": rate,
                        "threshold": 85,
                        "reason": "Forex rate exceeded threshold"
                    })

                elif max_rate and rate == max_rate:
                    events.append({
                        "type": "forex_recent_high",
                        "domain": "forex",
                        "entity": node["pair"],
                        "value": rate,
                        "reason": "Recent highest forex rate"
                    })

        # -------------------
        # SEVERITY LOGIC
        # -------------------
        count = len(events)

        if count >= 5:
            severity = "high"
        elif count >= 2:
            severity = "medium"
        else:
            severity = "low"

        decision_result = {
            "events": events,
            "count": count,
            "severity": severity,
            "requires_action": count > 0,
            "decision_timestamp": datetime.now().isoformat(),
            "summary": f"{count} decision events generated."
        }
        
        print("\n[DECISION NODE OUTPUT]")
        print(decision_result)

        return {
            "decision": decision_result,
            "langfuse_parent_span": parent
        }

    finally:
        if span:
            span.end()
    

# ACTION NODE
def action_node(state: AgentState) -> AgentState:
    parent = state.get("langfuse_parent_span")
    span = parent.start_span(name="action") if parent else None

    try:
        decision_result = state.get("decision", {})

        if decision_result.get("requires_action"):
            result = trigger_alerts(decision_result)
        else:
            result = "No Action Needed"

        print("\n[ACTION NODE OUTPUT]")
        print(result)
        return {
            "action": result,
            "langfuse_parent_span": parent
        }

    finally:
        if span:
            span.end()

# BUILD GRAPH
def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("process", processing_node)
    builder.add_node("analyze", analysis_node)
    builder.add_node("decide", decision_node)
    builder.add_node("act", action_node)
    builder.add_node("knowledge_retrieval", knowledge_retrieval)

    builder.set_entry_point("process")

    # builder.add_edge("process", "analyze")
    builder.add_edge("process", "knowledge_retrieval")
    builder.add_edge("knowledge_retrieval", "analyze")
    builder.add_edge("analyze", "decide")
    builder.add_edge("decide", "act")

    builder.set_finish_point("act")

    return builder.compile()