from npcpy import tool, agent, AgentExecutor
from project_starter import (
    get_all_inventory,
    get_stock_level,
    get_cash_balance,
    get_supplier_delivery_date,
    create_transaction,
    generate_financial_report,
    search_quote_history,
    run_test_scenarios,
)

# ------------------- TOOLS -------------------

@tool
def get_all_inventory_tool():
    """Get the full inventory list."""
    return get_all_inventory()

@tool
def get_stock_level_tool(item_name: str):
    """Check stock level for a specific item."""
    return get_stock_level(item_name)

@tool
def get_cash_balance_tool():
    """Retrieve current cash balance."""
    return get_cash_balance()

@tool
def search_quote_history_tool(query: str):
    """Search historical quotes for reference."""
    return search_quote_history(query)

@tool
def create_transaction_tool(transaction_details: str):
    """Finalize a transaction and update inventory."""
    return create_transaction(transaction_details)

@tool
def generate_financial_report_tool():
    """Generate a financial summary."""
    return generate_financial_report()

@tool
def get_supplier_delivery_date_tool(item_name: str):
    """Estimate supplier delivery time."""
    return get_supplier_delivery_date(item_name)


# ------------------- AGENTS -------------------

@agent(
    tools=[
        get_all_inventory_tool,
        get_stock_level_tool,
        get_cash_balance_tool,
    ],
    description="Check inventory, assess reorder needs, and provide availability updates.",
)
def inventory_agent(task: str) -> str:
    return f"Received task: {task}"


@agent(
    tools=[
        search_quote_history_tool,
    ],
    description="Generate accurate and competitive price quotes using historical data.",
)
def quote_agent(task: str) -> str:
    return f"Received task: {task}"


@agent(
    tools=[
        create_transaction_tool,
        generate_financial_report_tool,
    ],
    description="Process orders, update inventory, and record transactions.",
)
def sales_agent(task: str) -> str:
    return f"Received task: {task}"


@agent(
    tools=[
        get_supplier_delivery_date_tool,
    ],
    description="Estimate delivery timelines using supplier information.",
)
def delivery_agent(task: str) -> str:
    return f"Received task: {task}"


# ------------------- ORCHESTRATOR -------------------

def orchestrator_agent(request_text: str) -> str:
    inventory_result = inventory_agent.run(f"The customer requested: {request_text}. What is the stock status of the requested items?")
    quote_result = quote_agent.run(f"The customer requested: {request_text}. Use historical data to suggest a price quote.")
    sales_result = sales_agent.run(f"We have generated a quote and customer agreed. Process the transaction for: {request_text}")
    delivery_result = delivery_agent.run(f"Provide estimated delivery date for: {request_text}")

    return (
        f"Inventory Check:\n{inventory_result}\n\n"
        f"Quote:\n{quote_result}\n\n"
        f"Sales Processing:\n{sales_result}\n\n"
        f"Delivery Estimate:\n{delivery_result}\n"
    )


# ------------------- TEST HARNESS -------------------

if __name__ == "__main__":
    run_test_scenarios(orchestrator_agent)