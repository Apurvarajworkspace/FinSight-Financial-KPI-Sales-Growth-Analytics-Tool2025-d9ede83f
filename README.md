# FinSight — Financial KPI & Sales Growth Analytics Tool

FinSight is a Python analytics toolkit for cleaning and validating business datasets, calculating core financial KPIs, forecasting trends, and generating visual reports. The repository includes modules for revenue analysis, customer segmentation, churn evaluation, forecasting, SQL extraction, and HTML report output.

## What the code shows

The project contains evidence for the following workflows:

- CSV loading, validation, cleaning, type conversion, and aggregation
- Revenue, profit, churn, and customer-segmentation calculations
- Forecasting modules, including CAGR and exponential smoothing approaches
- SQL/MySQL extraction and join-based workflows
- Visualization layers using Plotly, Seaborn, and Matplotlib
- HTML report generation and export-oriented modules

## Key modules

```text
main.py                  Entry point for command modes
config.py                Runtime configuration and defaults
data_processor.py        Data loading and cleaning
kpi_calculator.py        KPI logic
sql_extractor.py         MySQL extraction and query handling
forecasting_module.py    Forecasting and growth calculations
report_generator.py      Weekly/monthly report generation
visualization_engine.py  Chart and visualization generation
advanced_*.py            Additional analytics modules
```

## Technology stack

- Python
- Pandas
- NumPy
- SciPy
- scikit-learn
- Plotly
- Seaborn
- Matplotlib
- MySQL Connector/Python
- SQLAlchemy
- OpenPyXL

## Setup

```bash
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
# .venv\Scripts\activate        # Windows PowerShell
pip install -r requirements.txt
```

## Usage

The repository documents the following commands:

```bash
python main.py --mode demo
python main.py --mode process --input data/sales_data.csv
python main.py --mode analyze --input data/sales_data.csv
python main.py --mode report --input data/sales_data.csv
```

## Database configuration

`config.py` currently contains local development defaults, including a database host, credentials, and timeouts. Do not commit real database credentials. The safer pattern is to move these values into environment variables or a local `.env` file that is excluded from source control.

## Security note

A basic review identified a hard-coded database password placeholder in `config.py`:

```python
'password': 'password'
```

This may be just a sample value, but it should not remain in source code for any production or shared environment.

## Project organization

```text
reports/                Generated output and HTML reports
exports/                Export-oriented modules and outputs
test_env/               Environment/test workspace
advanced_*_module.py    Advanced analytics modules
README.md               Project overview
requirements.txt        Dependency list
```

## Important notes

- SQL extraction only works when a compatible MySQL server and schema are configured.
- Forecasting and KPI outputs depend on the quality and structure of the input data.
- This project is best understood as a Python analytics workflow and prototype rather than a production-grade finance platform.

## Best next steps

- Move database settings to environment variables
- Add unit tests for invalid schema handling and KPI edge cases
- Add CI for dependency installation and import checks
- Add a reproducible sample dataset and example output screenshots

## Author

Built by [Apurva Raj](https://github.com/Apurvaraj08).
