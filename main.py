from smolagents import Tool, Agent, AgentExecutor
from project_starter import (
    get_all_inventory,
    get_stock_level,
    get_cash_balance,
    get_supplier_delivery_date,
    create_transaction,
    generate_financial_report,
    search_quote_history,
    run_test_scenarios
)

# Inventory Tools
inventory_tools = [
    Tool(name="get_all_inventory", func=get_all_inventory, description="Get the full inventory list."),
    Tool(name="get_stock_level", func=get_stock_level, description="Check stock level for a specific item."),
    Tool(name="get_cash_balance", func=get_cash_balance, description="Retrieve current cash balance."),
]

# Quoting Tools
quote_tools = [
    Tool(name="search_quote_history", func=search_quote_history, description="Search historical quotes for reference."),
]

# Sales Tools
sales_tools = [
    Tool(name="create_transaction", func=create_transaction, description="Finalize a transaction and update inventory."),
    Tool(name="generate_financial_report", func=generate_financial_report, description="Generate a financial summary."),
]

# Delivery Tools
delivery_tools = [
    Tool(name="get_supplier_delivery_date", func=get_supplier_delivery_date, description="Estimate supplier delivery time."),
]

# Inventory Agent
inventory_agent = Agent(
    role="Inventory Manager",
    goal="Check inventory, assess reorder needs, and provide availability updates.",
    tools=inventory_tools,
)

# Quote Agent
quote_agent = Agent(
    role="Quotation Specialist",
    goal="Generate accurate and competitive price quotes using historical data and customer request.",
    tools=quote_tools,
)

# Sales Agent
sales_agent = Agent(
    role="Sales Processor",
    goal="Process successful orders, update inventory, and record transactions.",
    tools=sales_tools,
)

# Delivery Agent
delivery_agent = Agent(
    role="Delivery Scheduler",
    goal="Provide expected delivery timelines using supplier information.",
    tools=delivery_tools,
)


# Orchestrator Agent
def orchestrator_agent(request_text: str) -> str:
    # Check Inventory
    inventory_result = inventory_agent(f"The customer requested: {request_text}. What is the stock status of the requested items?")

    # Generate Quote
    quote_result = quote_agent(f"The customer requested: {request_text}. Use historical data to suggest a price quote.")

    # Process Order
    sales_result = sales_agent(f"We have generated a quote and customer agreed. Process the transaction for: {request_text}")

    # Estimate Delivery
    delivery_result = delivery_agent(f"Provide estimated delivery date for: {request_text}")

    # Combine customer-facing response
    final_response = (
        f"Inventory Check:\n{inventory_result}\n\n"
        f"Quote:\n{quote_result}\n\n"
        f"Sales Processing:\n{sales_result}\n\n"
        f"Delivery Estimate:\n{delivery_result}\n"
    )
    return final_response

# Run evaluation on sample data
if __name__ == "__main__":
    run_test_scenarios(orchestrator_agent)