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