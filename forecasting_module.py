"""
Forecasting Module
Handles CAGR calculation, exponential smoothing forecasts, and CLV computation
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from config import FORECAST_CONFIG


class ForecastingModule:
    """Performs financial forecasting and predictive analytics"""
    
    def __init__(self, config: Dict = None):
        """Initialize Forecasting Module with configuration"""
        self.config = config or FORECAST_CONFIG
    
    def calculate_cagr(self, beginning_value: float, ending_value: float,
                      num_years: float) -> float:
        """
        Calculate Compound Annual Growth Rate
        
        Args:
            beginning_value: Starting value
            ending_value: Ending value
            num_years: Number of years
            
        Returns:
            CAGR as percentage
            
        Raises:
            ValueError: If inputs are invalid
        """
        # Validate beginning value
        if beginning_value is None or pd.isna(beginning_value):
            raise ValueError("Beginning value cannot be NULL")
        if beginning_value <= 0:
            raise ValueError(f"Beginning value must be positive, got {beginning_value}")
        
        # Validate ending value
        if ending_value is None or pd.isna(ending_value):
            raise ValueError("Ending value cannot be NULL")
        if ending_value <= 0:
            raise ValueError(f"Ending value must be positive, got {ending_value}")
        
        # Validate number of years
        if num_years is None or pd.isna(num_years):
            raise ValueError("Number of years cannot be NULL")
        if num_years <= 0 or num_years > 100:
            raise ValueError(f"Number of years must be between 1 and 100, got {num_years}")
        
        # Calculate CAGR
        cagr = (pow(ending_value / beginning_value, 1 / num_years) - 1) * 100
        
        decimal_places = self.config.get('cagr_decimal_places', 2)
        return round(cagr, decimal_places)
    
    def calculate_cagr_for_metrics(self, df: pd.DataFrame, metrics: List[str],
                                   start_date: str, end_date: str,
                                   date_column: str = 'date') -> Dict[str, float]:
        """
        Calculate CAGR for multiple metrics
        
        Args:
            df: DataFrame with time-series data
            metrics: List of metric columns
            start_date: Start date
            end_date: End date
            date_column: Name of date column
            
        Returns:
            Dictionary mapping metric names to CAGR values
        """
        df_copy = df.copy()
        df_copy[date_column] = pd.to_datetime(df_copy[date_column])
        
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        # Calculate number of years
        num_years = (end_date - start_date).days / 365.25
        
        results = {}
        for metric in metrics:
            if metric not in df.columns:
                raise ValueError(f"Metric column '{metric}' not found")
            
            # Get beginning and ending values
            beginning_value = df_copy[df_copy[date_column] <= start_date][metric].sum()
            ending_value = df_copy[df_copy[date_column] <= end_date][metric].sum()
            
            try:
                cagr = self.calculate_cagr(beginning_value, ending_value, num_years)
                results[metric] = cagr
            except ValueError as e:
                results[metric] = None
        
        return results
    
    def exponential_smoothing_forecast(self, historical_data: List[float],
                                      alpha: float = None,
                                      forecast_periods: int = 1) -> Dict:
        """
        Generate sales forecast using exponential smoothing
        
        Args:
            historical_data: List of historical values
            alpha: Smoothing parameter (0 < alpha <= 1)
            forecast_periods: Number of periods to forecast
            
        Returns:
            Dictionary with forecasts and historical data
            
        Raises:
            ValueError: If inputs are invalid
        """
        # Validate historical data
        if not historical_data or len(historical_data) < 3:
            raise ValueError(f"Minimum 3 data points required, got {len(historical_data) if historical_data else 0}")
        
        if len(historical_data) > 10000:
            raise ValueError(f"Maximum 10,000 data points allowed, got {len(historical_data)}")
        
        # Validate alpha
        alpha = alpha or self.config.get('default_alpha', 0.3)
        if alpha <= 0 or alpha > 1:
            raise ValueError(f"Alpha must be between 0 and 1 (exclusive of 0), got {alpha}")
        
        # Validate forecast periods
        max_periods = self.config.get('max_forecast_periods', 365)
        if forecast_periods < 1 or forecast_periods > max_periods:
            raise ValueError(f"Forecast periods must be between 1 and {max_periods}, got {forecast_periods}")
        
        # Check for invalid data
        if any(pd.isna(x) for x in historical_data):
            raise ValueError("Historical data contains NULL values")
        
        if not all(isinstance(x, (int, float)) for x in historical_data):
            raise ValueError("Historical data must contain only numeric values")
        
        # Perform exponential smoothing
        smoothed = [historical_data[0]]
        
        for i in range(1, len(historical_data)):
            smoothed_value = alpha * historical_data[i] + (1 - alpha) * smoothed[i-1]
            smoothed.append(smoothed_value)
        
        # Generate forecasts
        forecasts = []
        last_smoothed = smoothed[-1]
        
        for _ in range(forecast_periods):
            forecasts.append(last_smoothed)
        
        return {
            'historical_data': historical_data,
            'smoothed_values': smoothed,
            'forecasts': forecasts,
            'alpha': alpha,
            'forecast_periods': forecast_periods
        }
    
    def calculate_customer_lifetime_value(self, df: pd.DataFrame,
                                         customer_column: str = 'customer_id',
                                         amount_column: str = 'amount',
                                         date_column: str = 'date') -> pd.DataFrame:
        """
        Calculate Customer Lifetime Value
        
        Args:
            df: DataFrame with customer transaction data
            customer_column: Name of customer ID column
            amount_column: Name of transaction amount column
            date_column: Name of date column
            
        Returns:
            DataFrame with CLV for each customer
            
        Raises:
            ValueError: If data is insufficient
        """
        required_cols = [customer_column, amount_column, date_column]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
        
        df_copy = df.copy()
        df_copy[date_column] = pd.to_datetime(df_copy[date_column])
        
        # Filter customers with at least 2 transactions
        transaction_counts = df_copy.groupby(customer_column).size()
        valid_customers = transaction_counts[transaction_counts >= 2].index
        
        if len(valid_customers) == 0:
            raise ValueError("Insufficient transaction data: No customers with 2+ transactions")
        
        df_filtered = df_copy[df_copy[customer_column].isin(valid_customers)]
        
        # Calculate metrics per customer
        customer_metrics = []
        
        for customer_id in valid_customers:
            customer_data = df_filtered[df_filtered[customer_column] == customer_id]
            
            # Average purchase value
            avg_purchase_value = customer_data[amount_column].mean()
            
            # Purchase frequency (transactions per year)
            first_transaction = customer_data[date_column].min()
            last_transaction = customer_data[date_column].max()
            days_active = (last_transaction - first_transaction).days
            
            if days_active == 0:
                days_active = 1
            
            num_transactions = len(customer_data)
            purchase_frequency = (num_transactions / days_active) * 365
            
            # Customer lifespan (in years)
            customer_lifespan = days_active / 365.25
            if customer_lifespan == 0:
                customer_lifespan = 1 / 365.25  # Minimum 1 day
            
            # Calculate CLV
            clv = avg_purchase_value * purchase_frequency * customer_lifespan
            
            customer_metrics.append({
                customer_column: customer_id,
                'avg_purchase_value': round(avg_purchase_value, 2),
                'purchase_frequency': round(purchase_frequency, 2),
                'customer_lifespan_years': round(customer_lifespan, 2),
                'clv': round(clv, 2),
                'num_transactions': num_transactions
            })
        
        return pd.DataFrame(customer_metrics)
    
    def calculate_segment_clv(self, df: pd.DataFrame, segment_column: str,
                             customer_column: str = 'customer_id',
                             amount_column: str = 'amount',
                             date_column: str = 'date') -> pd.DataFrame:
        """
        Calculate CLV for customer segments
        
        Args:
            df: DataFrame with customer transaction data
            segment_column: Column defining customer segments
            customer_column: Name of customer ID column
            amount_column: Name of transaction amount column
            date_column: Name of date column
            
        Returns:
            DataFrame with average CLV per segment
        """
        if segment_column not in df.columns:
            raise ValueError(f"Segment column '{segment_column}' not found")
        
        # Calculate individual CLV
        clv_df = self.calculate_customer_lifetime_value(df, customer_column, amount_column, date_column)
        
        # Merge with segment information
        customer_segments = df[[customer_column, segment_column]].drop_duplicates()
        clv_with_segments = clv_df.merge(customer_segments, on=customer_column)
        
        # Calculate average CLV per segment
        segment_clv = clv_with_segments.groupby(segment_column).agg({
            'clv': 'mean',
            'avg_purchase_value': 'mean',
            'purchase_frequency': 'mean',
            'customer_lifespan_years': 'mean',
            customer_column: 'count'
        }).reset_index()
        
        segment_clv.rename(columns={customer_column: 'num_customers'}, inplace=True)
        segment_clv = segment_clv.round(2)
        
        return segment_clv
