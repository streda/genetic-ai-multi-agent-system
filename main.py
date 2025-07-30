from pydantic_ai import Agent, Tool
import asyncio

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine
from project_starter import (
    get_all_inventory,
    get_stock_level,
    get_cash_balance,
    get_supplier_delivery_date,
    create_transaction,
    generate_financial_report,
    search_quote_history,
    run_test_scenarios,
    init_database  
)

# Create database engine
db_engine = create_engine("sqlite:///beavers_choice.db")

# Initialize database
init_database(db_engine)


from project_starter import get_stock_level as _get_stock_level
from typing import Union
import pandas as pd
from datetime import datetime

from project_starter import get_stock_level as _get_stock_level

def get_stock_level_serializable(item_name: str, as_of_date: Union[str, datetime]) -> dict:
    df = _get_stock_level(item_name, as_of_date)
    if df.empty:
        return {"item_name": item_name, "current_stock": 0}
    row = df.iloc[0]
    return {"item_name": str(row["item_name"]), "current_stock": int(row["current_stock"])}

inventory_tools = [
    Tool(get_all_inventory, name="get_all_inventory", description="Get the full inventory list."),
    Tool(get_stock_level_serializable, name="get_stock_level", description="Check stock level for a specific item."),
    Tool(get_cash_balance, name="get_cash_balance", description="Retrieve current cash balance."),
]

# Quote Tools
quote_tools = [
    Tool(search_quote_history, name="search_quote_history", description="Search historical quotes for reference."),
]

# Sales Tools
sales_tools = [
    Tool(create_transaction, name="create_transaction", description="Finalize a transaction and update inventory."),
    Tool(generate_financial_report, name="generate_financial_report", description="Generate a financial summary."),
]

# Delivery Tools
delivery_tools = [
    Tool(get_supplier_delivery_date, name="get_supplier_delivery_date", description="Estimate supplier delivery time."),
]

# Agents
inventory_agent = Agent(
    role="Inventory Manager",
    goal="Check inventory, assess reorder needs, and provide availability updates.",
    tools=inventory_tools,  
    model="gpt-4o",
)

quote_agent = Agent(
    role="Quotation Specialist",
    goal="Generate accurate and competitive price quotes using historical data and customer request.",
    tools=quote_tools,
    model="gpt-4o",
)

sales_agent = Agent(
    role="Sales Processor",
    goal="Process successful orders, update inventory, and record transactions.",
    tools=sales_tools,
    model="gpt-4o",
)

delivery_agent = Agent(
    role="Delivery Scheduler",
    goal="Provide expected delivery timelines using supplier information.",
    tools=delivery_tools,
    model="gpt-4o",
)

import asyncio, json
from pydantic_ai.agent import AgentRunResult

db_lock = asyncio.Lock()

async def safe_create_transaction(
    item_name: str,
    transaction_type: str,
    quantity: int,
    price: float,
    date: Union[str, datetime],
) -> int:
    async with db_lock:
        return create_transaction(item_name, transaction_type, quantity, price, date)

sales_tools = [
    Tool(safe_create_transaction,
         name="create_transaction",
         description="Finalize a transaction and update inventory safely."),
    Tool(generate_financial_report, name="generate_financial_report", description="Generate a financial summary."),
]

async def run_and_unwrap(agent, prompt):
    raw = await agent.run(prompt)
    if isinstance(raw, AgentRunResult):
        raw = raw.output
    if not isinstance(raw, str):
        raw = json.dumps(raw, ensure_ascii=False)
    return raw

# Orchestrator Agent
async def orchestrator_agent(request_text: str) -> str:
    inv = await run_and_unwrap(inventory_agent,
        f"The customer requested: {request_text}. What is the stock status?"
    )
    quote = await run_and_unwrap(quote_agent,
        f"…generate a quote with rationale…"
    )
    sales = await run_and_unwrap(sales_agent,
        f"…process transaction…"
    )
    deliver = await run_and_unwrap(delivery_agent,
        f"…estimate delivery…"
    )

    return (
        f"Inventory Availability:\n{inv}\n\n"
        f"Quote Summary:\n{quote}\n\n"
        f"Order Confirmation:\n{sales}\n\n"
        f"Delivery Estimate:\n{deliver}"
    )

# Run tests
if __name__ == "__main__":
    init_database(db_engine)
    # Save test results to test_results.csv
    run_test_scenarios(lambda request: asyncio.run(orchestrator_agent(request)))