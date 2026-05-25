"""
Configuration settings for the Financial KPI Analytics Tool
"""

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'username': 'root',
    'password': 'password',
    'database': 'financial_db'
}

# Data Processing Configuration
DATA_CONFIG = {
    'missing_value_strategy': 'drop',  # Options: 'drop', 'fill_mean', 'fill_median', 'fill_zero'
    'remove_duplicates': True,
    'date_column': 'date',
    'required_columns': ['date', 'revenue', 'cost', 'customer_id']
}

# KPI Calculation Configuration
KPI_CONFIG = {
    'high_performing_percentile': 90,  # Top 10%
    'underperforming_percentile': 10,  # Bottom 10%
    'churn_inactivity_days': 90,
    'min_segments_for_ranking': 3
}

# Forecasting Configuration
FORECAST_CONFIG = {
    'default_alpha': 0.3,
    'min_data_points': 3,
    'max_forecast_periods': 365,
    'cagr_decimal_places': 2
}

# SQL Configuration
SQL_CONFIG = {
    'query_timeout': 60,  # seconds
    'connection_timeout': 30,  # seconds
    'max_query_timeout': 300  # seconds for data extraction
}

# Reporting Configuration
REPORT_CONFIG = {
    'output_directory': 'reports',
    'weekly_report_day': 'Monday',
    'monthly_report_day': 1,
    'report_format': 'html'
}

# Visualization Configuration
VIZ_CONFIG = {
    'heatmap_colorscale': 'RdYlGn',
    'chart_height': 600,
    'chart_width': 1000,
    'max_categories': 50,
    'image_format': 'png',
    'image_dpi': 300
}

# Rolling Average Windows
ROLLING_WINDOWS = {
    'short': 7,   # 7-day
    'medium': 30,  # 30-day
    'long': 90    # 90-day
}
