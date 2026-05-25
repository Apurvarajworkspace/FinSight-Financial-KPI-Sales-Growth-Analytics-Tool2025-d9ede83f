# Financial KPI Analytics Tool

A comprehensive data analytics tool designed to calculate, track, and visualize key financial KPIs and sales growth metrics from raw business datasets — built to mirror real-world fintech data analyst workflows.

## Features

### Data Processing
- **CSV Data Loading**: Load and validate raw sales and financial CSV datasets
- **Data Cleaning**: Handle missing values, remove duplicates, and convert data types
- **Data Transformation**: Aggregate, pivot, merge, and transform datasets
- **Validation**: Ensure data quality with required column validation

### KPI Calculations
- **Revenue Metrics**: Calculate total revenue, revenue growth rates (period-over-period, year-over-year)
- **Profit Analysis**: Compute gross profit margins at transaction, product, and aggregate levels
- **Customer Churn**: Calculate customer churn rates for weekly, monthly, and quarterly periods
- **Segment Analysis**: Identify high-performing and underperforming business segments

### Database Integration
- **MySQL Connectivity**: Extract data from MySQL databases with optimized queries
- **Multi-table Joins**: Support for INNER, LEFT, and RIGHT JOIN operations
- **Window Functions**: Calculate rolling averages for sales trend analysis
- **Query Optimization**: Indexed joins, filtered queries, and timeout management

### Advanced Analytics
- **CAGR Calculation**: Compute Compound Annual Growth Rate for revenue, profit, and customer metrics
- **Sales Forecasting**: Exponential smoothing for predictive sales analysis
- **Customer Lifetime Value**: Calculate CLV for individual customers and segments

### Reporting & Visualization
- **Automated Reports**: Generate weekly and monthly financial summaries with trend comparisons
- **Interactive Charts**: Plotly-based line charts, bar charts, and multi-series visualizations
- **Statistical Visualizations**: Seaborn heatmaps and bar charts for pattern identification
- **HTML Reports**: Interactive HTML reports with embedded visualizations

## Tech Stack

- **Python 3.8+**
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Plotly**: Interactive visualizations
- **Seaborn**: Statistical data visualization
- **Matplotlib**: Plotting library
- **MySQL Connector**: Database connectivity
- **SQLAlchemy**: SQL toolkit

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd financial-kpi-analytics-tool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure database settings (optional):
Edit `config.py` to set your MySQL database credentials:
```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'username': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}
```

## Usage

### Demo Mode
Run the demo to see all features in action with sample data:
```bash
python main.py --mode demo
```

### Process CSV Data
```bash
python main.py --mode process --input data/sales_data.csv
```

### Analyze Data
```bash
python main.py --mode analyze --input data/sales_data.csv
```

### Generate Reports
```bash
python main.py --mode report --input data/sales_data.csv
```

### Programmatic Usage

```python
from data_processor import DataProcessor
from kpi_calculator import KPICalculator
from forecasting_module import ForecastingModule
from visualization_engine import VisualizationEngine

# Load and process data
processor = DataProcessor()
df = processor.process_csv('sales_data.csv')

# Calculate KPIs
calculator = KPICalculator()
total_revenue = calculator.calculate_total_revenue(df)
growth_df = calculator.calculate_revenue_growth(df, period_type='month')
churn_metrics = calculator.calculate_churn_rate(df)

# Forecasting
forecasting = ForecastingModule()
cagr = forecasting.calculate_cagr(100000, 150000, 3)
clv_df = forecasting.calculate_customer_lifetime_value(df)

# Visualizations
viz = VisualizationEngine()
fig = viz.create_line_chart(df, 'date', 'revenue', title='Revenue Trend')
viz.embed_in_html([fig], 'report.html')
```

## Project Structure

```
financial-kpi-analytics-tool/
├── main.py                    # Main application entry point
├── config.py                  # Configuration settings
├── data_processor.py          # Data loading and processing
├── kpi_calculator.py          # KPI calculations
├── sql_extractor.py           # MySQL database extraction
├── forecasting_module.py      # Forecasting and predictive analytics
├── report_generator.py        # Automated report generation
├── visualization_engine.py    # Visualization creation
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── reports/                   # Generated reports directory
```

## Module Documentation

### DataProcessor
Handles CSV loading, data cleaning, validation, aggregation, and transformation.

**Key Methods:**
- `load_csv()`: Load CSV files into DataFrames
- `handle_missing_values()`: Handle missing data with configurable strategies
- `remove_duplicates()`: Remove duplicate records
- `aggregate_data()`: Perform grouping and aggregation
- `pivot_data()`: Transform data from long to wide format
- `merge_datasets()`: Merge multiple datasets

### KPICalculator
Calculates financial KPIs including revenue growth, profit margins, and churn rates.

**Key Methods:**
- `calculate_total_revenue()`: Compute total revenue for time periods
- `calculate_revenue_growth()`: Calculate period-over-period growth
- `calculate_profit_margin()`: Compute gross profit margins
- `calculate_churn_rate()`: Calculate customer churn rates
- `identify_segments()`: Identify high/underperforming segments

### SQLExtractor
Extracts data from MySQL databases with optimized queries.

**Key Methods:**
- `connect()`: Establish database connection
- `execute_query()`: Execute SELECT queries
- `execute_join_query()`: Perform multi-table joins
- `calculate_rolling_average()`: Compute rolling averages with window functions
- `execute_aggregation_query()`: Execute GROUP BY queries

### ForecastingModule
Performs financial forecasting and predictive analytics.

**Key Methods:**
- `calculate_cagr()`: Calculate Compound Annual Growth Rate
- `exponential_smoothing_forecast()`: Generate sales forecasts
- `calculate_customer_lifetime_value()`: Compute CLV
- `calculate_segment_clv()`: Calculate CLV by customer segment

### VisualizationEngine
Creates interactive and statistical visualizations.

**Key Methods:**
- `create_line_chart()`: Create interactive line charts with Plotly
- `create_bar_chart()`: Create interactive bar charts
- `create_heatmap()`: Create correlation heatmaps with Seaborn
- `embed_in_html()`: Embed visualizations in HTML reports

### ReportGenerator
Generates automated weekly and monthly financial reports.

**Key Methods:**
- `generate_weekly_report()`: Create weekly financial summaries
- `generate_monthly_report()`: Create monthly financial summaries

## Configuration

Edit `config.py` to customize:
- Database connection settings
- Data processing strategies
- KPI calculation parameters
- Forecasting defaults
- Visualization styles
- Report output settings

## Sample Data Format

The tool expects CSV files with the following columns:
- `date`: Transaction date (YYYY-MM-DD)
- `customer_id`: Unique customer identifier
- `revenue`: Revenue amount
- `cost`: Cost amount
- `product_category`: Product category (optional)
- `region`: Geographic region (optional)

## Output

### Reports
Generated reports are saved in the `reports/` directory:
- Weekly reports: `weekly_report_YYYYMMDD.html`
- Monthly reports: `monthly_report_YYYYMM.html`

### Visualizations
- Interactive HTML reports with embedded Plotly charts
- Static PNG/SVG images for heatmaps and statistical charts

## Error Handling

The tool includes comprehensive error handling:
- Missing required columns
- Invalid data types
- Database connection failures
- Insufficient data for calculations
- Query timeouts

## Performance Optimization

- Indexed database queries
- Efficient Pandas operations
- Configurable query timeouts
- Data validation before processing
- Memory-efficient data handling

## License

MIT License

## Contributing

Contributions are welcome! Please submit pull requests or open issues for bugs and feature requests.

## Support

For questions or issues, please open an issue on the repository.
