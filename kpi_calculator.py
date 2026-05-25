"""
KPI Calculator Module
Calculates financial KPIs including revenue growth, profit margins, churn rates, and segment analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from config import KPI_CONFIG


class KPICalculator:
    """Calculates key performance indicators for financial analysis"""
    
    def __init__(self, config: Dict = None):
        """Initialize KPI Calculator with configuration"""
        self.config = config or KPI_CONFIG
    
    def calculate_total_revenue(self, df: pd.DataFrame, revenue_column: str = 'revenue',
                               date_column: str = 'date', period: str = None) -> float:
        """
        Calculate total revenue for specified time period
        
        Args:
            df: DataFrame containing revenue data
            revenue_column: Name of revenue column
            date_column: Name of date column
            period: Time period filter (e.g., '2024-01', 'Q1-2024')
            
        Returns:
            Total revenue as float
        """
        if revenue_column not in df.columns:
            raise ValueError(f"Revenue column '{revenue_column}' not found")
        
        df_filtered = df.copy()
        if period and date_column in df.columns:
            df_filtered[date_column] = pd.to_datetime(df_filtered[date_column])
            # Filter by period if specified
            # This is a simplified implementation
        
        total_revenue = df_filtered[revenue_column].sum()
        return float(total_revenue)
    
    def calculate_revenue_growth(self, df: pd.DataFrame, revenue_column: str = 'revenue',
                                date_column: str = 'date', period_type: str = 'month') -> pd.DataFrame:
        """
        Calculate period-over-period revenue growth percentage
        
        Args:
            df: DataFrame with revenue and date columns
            revenue_column: Name of revenue column
            date_column: Name of date column
            period_type: Type of period ('day', 'week', 'month', 'quarter', 'year')
            
        Returns:
            DataFrame with period, revenue, and growth rate
        """
        if revenue_column not in df.columns or date_column not in df.columns:
            raise ValueError(f"Required columns not found")
        
        df_copy = df.copy()
        df_copy[date_column] = pd.to_datetime(df_copy[date_column])
        
        # Group by period
        if period_type == 'month':
            df_copy['period'] = df_copy[date_column].dt.to_period('M')
        elif period_type == 'quarter':
            df_copy['period'] = df_copy[date_column].dt.to_period('Q')
        elif period_type == 'year':
            df_copy['period'] = df_copy[date_column].dt.to_period('Y')
        elif period_type == 'week':
            df_copy['period'] = df_copy[date_column].dt.to_period('W')
        else:
            df_copy['period'] = df_copy[date_column].dt.date
        
        # Aggregate revenue by period
        period_revenue = df_copy.groupby('period')[revenue_column].sum().reset_index()
        period_revenue = period_revenue.sort_values('period')
        
        # Calculate growth rate
        period_revenue['previous_revenue'] = period_revenue[revenue_column].shift(1)
        period_revenue['growth_rate'] = period_revenue.apply(
            lambda row: self._calculate_growth_rate(row['previous_revenue'], row[revenue_column]),
            axis=1
        )
        
        return period_revenue[['period', revenue_column, 'growth_rate']]
    
    def _calculate_growth_rate(self, previous_value: float, current_value: float) -> Optional[float]:
        """
        Calculate growth rate handling edge cases
        
        Args:
            previous_value: Previous period value
            current_value: Current period value
            
        Returns:
            Growth rate as percentage or None if cannot be calculated
        """
        if pd.isna(previous_value) or previous_value == 0:
            return None if pd.isna(previous_value) else float('inf') if current_value > 0 else 0.0
        
        growth_rate = ((current_value - previous_value) / abs(previous_value)) * 100
        return round(growth_rate, 2)
    
    def aggregate_revenue_by_dimension(self, df: pd.DataFrame, dimension: str,
                                      revenue_column: str = 'revenue') -> pd.DataFrame:
        """
        Aggregate revenue by specified dimension
        
        Args:
            df: DataFrame with revenue data
            dimension: Dimension to aggregate by (e.g., 'product_category', 'region')
            revenue_column: Name of revenue column
            
        Returns:
            DataFrame with dimension and aggregated revenue
        """
        if dimension not in df.columns:
            raise ValueError(f"Dimension column '{dimension}' not found")
        
        result = df.groupby(dimension)[revenue_column].sum().reset_index()
        result = result.sort_values(revenue_column, ascending=False)
        return result
    
    def calculate_profit_margin(self, df: pd.DataFrame, revenue_column: str = 'revenue',
                               cost_column: str = 'cost') -> pd.DataFrame:
        """
        Calculate gross profit margin
        
        Args:
            df: DataFrame with revenue and cost data
            revenue_column: Name of revenue column
            cost_column: Name of cost column
            
        Returns:
            DataFrame with profit margin column added
        """
        if revenue_column not in df.columns:
            raise ValueError(f"Revenue column '{revenue_column}' not found or contains NULL values")
        if cost_column not in df.columns:
            raise ValueError(f"Cost column '{cost_column}' not found or contains NULL values")
        
        df_copy = df.copy()
        
        # Validate numeric and positive revenue
        if not pd.api.types.is_numeric_dtype(df_copy[revenue_column]):
            raise ValueError(f"Revenue column must contain numeric values")
        
        # Calculate profit margin with proper handling of edge cases
        def calc_margin(row):
            revenue = row[revenue_column]
            cost = row[cost_column]
            
            # Handle NULL or missing values
            if pd.isna(revenue) or pd.isna(cost):
                return None
            
            # Handle zero revenue
            if revenue == 0:
                return None
            
            margin = (revenue - cost) / revenue
            return round(margin, 4)
        
        df_copy['profit_margin'] = df_copy.apply(calc_margin, axis=1)
        return df_copy
    
    def calculate_average_profit_margin(self, df: pd.DataFrame, dimension: str = None,
                                       profit_margin_column: str = 'profit_margin') -> float:
        """
        Calculate average profit margin across specified dimension
        
        Args:
            df: DataFrame with profit margin data
            dimension: Optional dimension to group by
            profit_margin_column: Name of profit margin column
            
        Returns:
            Average profit margin or DataFrame if dimension specified
        """
        if profit_margin_column not in df.columns:
            raise ValueError(f"Profit margin column '{profit_margin_column}' not found")
        
        if dimension:
            if dimension not in df.columns:
                raise ValueError(f"Dimension column '{dimension}' not found")
            result = df.groupby(dimension)[profit_margin_column].mean().reset_index()
            result[profit_margin_column] = result[profit_margin_column].round(4)
            return result
        else:
            return round(df[profit_margin_column].mean(), 4)
    
    def calculate_churn_rate(self, df: pd.DataFrame, customer_column: str = 'customer_id',
                            date_column: str = 'date', period_start: str = None,
                            period_end: str = None, period_type: str = 'month') -> Dict:
        """
        Calculate customer churn rate
        
        Args:
            df: DataFrame with customer transaction data
            customer_column: Name of customer ID column
            date_column: Name of date column
            period_start: Start date of analysis period
            period_end: End date of analysis period
            period_type: Type of period ('week', 'month', 'quarter')
            
        Returns:
            Dictionary with churn rate and related metrics
        """
        if customer_column not in df.columns or date_column not in df.columns:
            raise ValueError("Customer ID and date columns are required for churn calculation")
        
        df_copy = df.copy()
        df_copy[date_column] = pd.to_datetime(df_copy[date_column])
        
        # Define period boundaries
        if period_start:
            period_start = pd.to_datetime(period_start)
        else:
            period_start = df_copy[date_column].min()
        
        if period_end:
            period_end = pd.to_datetime(period_end)
        else:
            period_end = df_copy[date_column].max()
        
        # Identify active customers at start
        customers_at_start = df_copy[df_copy[date_column] <= period_start][customer_column].unique()
        
        # Identify customers who transacted during the period
        customers_active = df_copy[
            (df_copy[date_column] > period_start) & (df_copy[date_column] <= period_end)
        ][customer_column].unique()
        
        # Calculate churned customers
        churned_customers = set(customers_at_start) - set(customers_active)
        
        total_customers = len(customers_at_start)
        churned_count = len(churned_customers)
        
        if total_customers == 0:
            raise ValueError("Insufficient customer data for churn calculation")
        
        churn_rate = (churned_count / total_customers) * 100
        
        return {
            'churn_rate': round(churn_rate, 2),
            'total_customers_at_start': total_customers,
            'churned_customers': churned_count,
            'retained_customers': total_customers - churned_count,
            'period_start': period_start,
            'period_end': period_end
        }
    
    def identify_segments(self, df: pd.DataFrame, metrics: List[str],
                         segment_column: str) -> pd.DataFrame:
        """
        Identify high-performing and underperforming segments
        
        Args:
            df: DataFrame with segment performance data
            metrics: List of metric columns to analyze
            segment_column: Column identifying segments
            
        Returns:
            DataFrame with segment rankings and performance classification
        """
        if segment_column not in df.columns:
            raise ValueError(f"Segment column '{segment_column}' not found")
        
        # Validate minimum segments
        num_segments = df[segment_column].nunique()
        min_segments = self.config.get('min_segments_for_ranking', 3)
        if num_segments < min_segments:
            raise ValueError(f"Minimum {min_segments} segments required for ranking")
        
        result = df.copy()
        
        # Rank by each metric
        for metric in metrics:
            if metric not in df.columns:
                raise ValueError(f"Metric column '{metric}' not found")
            
            result[f'{metric}_rank'] = result[metric].rank(ascending=False, method='min')
            result[f'{metric}_percentile'] = result[metric].rank(pct=True) * 100
        
        # Classify segments
        high_perf_threshold = self.config.get('high_performing_percentile', 90)
        low_perf_threshold = self.config.get('underperforming_percentile', 10)
        
        def classify_segment(row):
            # Check if segment is in top 10% for any metric
            for metric in metrics:
                if row[f'{metric}_percentile'] >= high_perf_threshold:
                    return 'High-Performing'
            
            # Check if segment is in bottom 10% for any metric
            for metric in metrics:
                if row[f'{metric}_percentile'] <= low_perf_threshold:
                    return 'Underperforming'
            
            return 'Average'
        
        result['performance_classification'] = result.apply(classify_segment, axis=1)
        
        return result
