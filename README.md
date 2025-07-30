# Beavers Choice: Multi-Agent Paper Supplies Ordering System

This project implements a multi-agent AI system to automate the end-to-end workflow of taking customer paper-supply requests through inventory checking, quote generation, order processing, and delivery scheduling. It uses the **pydantic-ai** framework to orchestrate four specialist agents under one orchestrator and persists state in a SQLite database.

---

##  Features

- **Inventory Management**  
  - Tracks on-hand stock levels as of any date.  
  - Assesses reorder needs when stock is insufficient.  
  - Exposes a `get_all_inventory` and `get_stock_level` API.

- **Quotation Generation**  
  - Searches historical quotes for similar jobs.  
  - Generates competitive, explainable price quotes.  
  - Discounts and rationale are included in the customer-facing quote.

- **Sales Processing**  
  - Records confirmed transactions in the database.  
  - Updates inventory and cash balance.  
  - Produces a financial summary on demand via `generate_financial_report`.

- **Delivery Scheduling**  
  - Estimates supplier lead times based on order size.  
  - Returns a clear delivery date without leaking internal metrics.

- **Orchestrator Agent**  
  - Receives a single “customer request” string.  
  - Delegates to:
    1. **Inventory Manager**  
    2. **Quotation Specialist**  
    3. **Sales Processor**  
    4. **Delivery Scheduler**  
  - Aggregates their outputs into one coherent response.

- **End-to-End Test Harness**  
  - Reads a sample of 20 real-world requests from `quote_requests_sample.csv`.  
  - Runs each through the orchestrator, logs “before/after” cash, inventory, and AI responses.  
  - Outputs `test_results.csv` for analysis.

---

##  Getting Started

1. **Clone & install**  
   ```bash
   git clone <repo-url>
   cd genetic-ai-multi-agent-system
   python3 -m venv smolenv
   source smolenv/bin/activate
   pip install -r requirements.txt
   ```
2.	Configure OpenAI key
    ```
    echo "OPENAI_API_KEY=sk-…" > .env
    ```
3.	Initialize the database & run tests
    ```
    python main.py
    ```