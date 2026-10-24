# Smart Retail Analytics & Sales Forecasting System

A beginner-friendly Python data analytics project with a Streamlit dashboard, SQLite database, SQL queries, and a simple monthly sales forecasting demonstration.

## Important dataset note
`data/sales_data.csv` is a **synthetic sample dataset created for learning**. It is not real store data. Cost figures are assumed solely to demonstrate a profit-style metric; do not present them as real accounting profit.

## Features
- Load and clean sales data using Pandas
- Calculate revenue and average order value
- Analyse sales by month, product, category, and region
- Interactive dashboard with date, region, and category filters
- Download filtered data as CSV
- Save data to a SQLite database
- SQL examples for common business questions
- Simple linear-trend sales estimate with hold-out MAE comparison

## Setup (Windows / VS Code)
1. Install Python 3.10 or later and VS Code.
2. Open this folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
5. Activate it in PowerShell:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   If activation is blocked, open Command Prompt terminal and run:
   ```bat
   .venv\Scripts\activate.bat
   ```
6. Install packages:
   ```bash
   python -m pip install -r requirements.txt
   ```
7. Run the analysis script:
   ```bash
   python analysis.py
   ```
8. Launch the dashboard:
   ```bash
   python -m streamlit run dashboard.py
   ```
9. A browser tab should open with the dashboard. Keep the terminal running while using it.

## Project files
- `dashboard.py` — interactive dashboard and forecast demo
- `analysis.py` — beginner-friendly data-cleaning and summary script
- `data/sales_data.csv` — synthetic example data
- `sql_queries.sql` — SQLite business queries
- `requirements.txt` — required Python packages
- `project_report.docx` — editable report template
- `project_presentation.pptx` — editable presentation starter
- `screenshots/` — save your own screenshots here after running the dashboard

## Troubleshooting
- If `python` is not recognised, try `py` in place of `python`.
- If packages fail to install, check internet connectivity and confirm the terminal is using the same Python installation as VS Code.
- If Streamlit command is not found, use `python -m streamlit run dashboard.py`.
- Do not close the terminal while the dashboard is running 
