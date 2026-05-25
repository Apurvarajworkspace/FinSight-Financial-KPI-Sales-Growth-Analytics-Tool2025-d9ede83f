"""
Advanced Analytics Module
Provides advanced statistical analysis, anomaly detection, scenario analysis, and cohort analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from scipy import stats
from config import KPI_CONFIG


class AnomalyDetector:
    """Detects statistical anomalies in financial data"""
    
    def __init__(self, zscore_threshold: float = 3.0):
        """
        Initialize Anomaly Detector
        
        Args:
            zscore_threshold: Z-score threshold for anomaly detection (default: 3.0)
        """
        self.zscore_threshold = zscore_threshold
    
    def detect_zscore_anomalies(self, series: pd.Series, window: int = 20) -> Dict:
        """
        Detect anomalies using Z-score method with rolling window
        
        Args:
            series: Time series data
            window: Rolling window size
            
        Returns:
            Dictionary with anomaly indices, values, and z-scores
        """
        if len(series) < window:
            return {'anomalies': [], 'indices': [], 'z_scores': [], 'values': []}
        
        rolling_mean = series.rolling(window=window).mean()
        rolling_std = series.rolling(window=window).std()
        
        z_scores = np.abs((series - rolling_mean) / (rolling_std + 1e-8))
        anomaly_mask = z_scores > self.zscore_threshold
        
        return {
            'anomalies': anomaly_mask.sum(),
            'indices': np.where(anomaly_mask)[0].tolist(),
            'z_scores': z_scores[anomaly_mask].values.tolist(),
            'values': series[anomaly_mask].values.tolist()
        }
    
    def detect_iqr_anomalies(self, series: pd.Series, multiplier: float = 1.5) -> Dict:
        """
        Detect anomalies using Interquartile Range (IQR) method
        
        Args:
            series: Time series data
            multiplier: IQR multiplier for bounds (default: 1.5)
            
        Returns:
            Dictionary with anomaly details and bounds
        """
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        
        anomaly_mask = (series < lower_bound) | (series > upper_bound)
        
        return {
            'anomalies': anomaly_mask.sum(),
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'indices': np.where(anomaly_mask)[0].tolist(),
            'values': series[anomaly_mask].values.tolist()
        }


class ScenarioAnalyzer:
    """Performs what-if scenario analysis for financial metrics"""
    
    def __init__(self):
        """Initialize Scenario Analyzer"""
        pass
    
    def growth_scenario(self, current_value: float, growth_rates: List[float],
                       periods: int) -> Dict:
        """
        Project values under different growth rate scenarios
        
        Args:
            current_value: Starting value
            growth_rates: List of growth rate percentages (e.g., [5.0, 10.0, 15.0])
            periods: Number of periods to project
            
        Returns:
            Dictionary mapping scenario names to projected values
        """
        scenarios = {}
        
        for rate in growth_rates:
            projections = []
            value = current_value
            
            for _ in range(periods):
                value = value * (1 + rate / 100)
                projections.append(value)
            
            scenario_name = f"{rate:+.1f}% Growth"
            scenarios[scenario_name] = projections
        
        return scenarios
    
    def cost_reduction_scenario(self, base_revenue: float, base_cost: float,
                               cost_reduction_pcts: List[float]) -> Dict:
        """
        Analyze profit impact of cost reduction scenarios
        
        Args:
            base_revenue: Base revenue
            base_cost: Base cost
            cost_reduction_pcts: List of cost reduction percentages
            
        Returns:
            Dictionary with profit and margin impact for each scenario
        """
        scenarios = {}
        base_profit = base_revenue - base_cost
        base_margin = base_profit / base_revenue if base_revenue > 0 else 0
        
        for reduction_pct in cost_reduction_pcts:
            reduced_cost = base_cost * (1 - reduction_pct / 100)
            new_profit = base_revenue - reduced_cost
            new_margin = new_profit / base_revenue if base_revenue > 0 else 0
            profit_improvement = new_profit - base_profit
            margin_improvement = (new_margin - base_margin) * 100
            
            scenario_name = f"{reduction_pct:.1f}% Cost Reduction"
            scenarios[scenario_name] = {
                'new_cost': reduced_cost,
                'new_profit': new_profit,
                'new_margin': new_margin,
                'profit_improvement': profit_improvement,
                'margin_improvement': margin_improvement
            }
        
        return scenarios
    
    def revenue_price_elasticity(self, current_price: float, current_quantity: float,
                                price_changes: List[float],
                                elasticity: float = -1.0) -> Dict:
        """
        Analyze revenue under different price points with elasticity
        
        Args:
            current_price: Current price
            current_quantity: Current quantity sold
            price_changes: List of price change percentages
            elasticity: Price elasticity of demand (typically negative)
            
        Returns:
            Dictionary with quantity and revenue projections for each scenario
        """
        scenarios = {}
        
        for price_change in price_changes:
            new_price = current_price * (1 + price_change / 100)
            # Quantity change = elasticity * price change %
            quantity_change_pct = elasticity * price_change
            new_quantity = current_quantity * (1 + quantity_change_pct / 100)
            new_revenue = new_price * new_quantity
            revenue_change = new_revenue - (current_price * current_quantity)
            
            scenario_name = f"{price_change:+.1f}% Price Change"
            scenarios[scenario_name] = {
                'new_price': new_price,
                'new_quantity': new_quantity,
                'new_revenue': new_revenue,
                'revenue_change': revenue_change,
                'revenue_change_pct': (revenue_change / (current_price * current_quantity)) * 100 if (current_price * current_quantity) > 0 else 0
            }
        
        return scenarios


class CohortAnalyzer:
    """Performs cohort analysis to track customer groups over time"""
    
    def __init__(self):
        """Initialize Cohort Analyzer"""
        pass
    
    def create_cohorts(self, df: pd.DataFrame, customer_col: str = 'customer_id',
                      date_col: str = 'date', revenue_col: str = 'revenue',
                      cohort_period: str = 'M') -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Create customer cohorts based on acquisition date
        
        Args:
            df: DataFrame with customer transactions
            customer_col: Customer ID column name
            date_col: Date column name
            revenue_col: Revenue column name
            cohort_period: Cohort period ('D' for day, 'W' for week, 'M' for month)
            
        Returns:
            Tuple of (cohort_data DataFrame, cohort_sizes DataFrame)
        """
        df_cohort = df.copy()
        df_cohort[date_col] = pd.to_datetime(df_cohort[date_col])
        
        # Get first purchase date for each customer
        customer_first_purchase = df_cohort.groupby(customer_col)[date_col].min().reset_index()
        customer_first_purchase.columns = [customer_col, 'cohort_date']
        customer_first_purchase['cohort_date'] = customer_first_purchase['cohort_date'].dt.to_period(cohort_period)
        
        # Merge cohort date back to original data
        df_cohort = df_cohort.merge(customer_first_purchase, on=customer_col, how='left')
        df_cohort['transaction_period'] = df_cohort[date_col].dt.to_period(cohort_period)
        
        # Calculate cohort age (in periods)
        df_cohort['cohort_age'] = (df_cohort['transaction_period'] - df_cohort['cohort_date']).apply(lambda x: x.n)
        
        # Create cohort table
        cohort_data = df_cohort.groupby(['cohort_date', 'cohort_age'])[revenue_col].sum().reset_index()
        cohort_pivot = cohort_data.pivot_table(index='cohort_date', columns='cohort_age', 
                                               values=revenue_col, aggfunc='sum')
        
        # Cohort sizes (number of customers)
        cohort_sizes = df_cohort.groupby('cohort_date')[customer_col].nunique().reset_index()
        cohort_sizes.columns = ['cohort_date', 'cohort_size']
        
        return cohort_pivot, cohort_sizes
    
    def calculate_cohort_retention(self, df: pd.DataFrame, customer_col: str = 'customer_id',
                                   date_col: str = 'date', cohort_period: str = 'M') -> pd.DataFrame:
        """
        Calculate customer retention rates by cohort
        
        Args:
            df: DataFrame with customer transactions
            customer_col: Customer ID column name
            date_col: Date column name
            cohort_period: Cohort period
            
        Returns:
            DataFrame with retention rates by cohort age
        """
        df_ret = df.copy()
        df_ret[date_col] = pd.to_datetime(df_ret[date_col])
        
        # Get first purchase date
        customer_first_purchase = df_ret.groupby(customer_col)[date_col].min().reset_index()
        customer_first_purchase.columns = [customer_col, 'cohort_date']
        customer_first_purchase['cohort_date'] = customer_first_purchase['cohort_date'].dt.to_period(cohort_period)
        
        df_ret = df_ret.merge(customer_first_purchase, on=customer_col, how='left')
        df_ret['transaction_period'] = df_ret[date_col].dt.to_period(cohort_period)
        df_ret['cohort_age'] = (df_ret['transaction_period'] - df_ret['cohort_date']).apply(lambda x: x.n)
        
        # Unique customers per cohort period
        cohort_unique = df_ret.groupby(['cohort_date', 'cohort_age'])[customer_col].nunique().reset_index()
        cohort_unique.columns = ['cohort_date', 'cohort_age', 'unique_customers']
        
        # First period customers (baseline)
        cohort_sizes = df_ret.groupby('cohort_date')[customer_col].nunique().reset_index()
        cohort_sizes.columns = ['cohort_date', 'cohort_size']
        
        cohort_unique = cohort_unique.merge(cohort_sizes, on='cohort_date', how='left')
        cohort_unique['retention_rate'] = (cohort_unique['unique_customers'] / cohort_unique['cohort_size'] * 100).round(2)
        
        return cohort_unique[['cohort_date', 'cohort_age', 'retention_rate']]


class StatisticalAnalyzer:
    """Performs statistical analysis on financial metrics"""
    
    def __init__(self):
        """Initialize Statistical Analyzer"""
        pass
    
    def correlation_analysis(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Calculate correlation matrix for specified columns
        
        Args:
            df: DataFrame with data
            columns: List of column names to analyze
            
        Returns:
            Correlation matrix DataFrame
        """
        subset_df = df[columns].select_dtypes(include=[np.number])
        correlation = subset_df.corr()
        return correlation
    
    def distribution_analysis(self, series: pd.Series) -> Dict:
        """
        Analyze distribution characteristics of a series
        
        Args:
            series: Pandas Series with data
            
        Returns:
            Dictionary with distribution statistics
        """
        clean_series = series.dropna()
        
        skewness = stats.skew(clean_series)
        kurtosis = stats.kurtosis(clean_series)
        
        # Normality test (Shapiro-Wilk)
        if len(clean_series) > 2:
            normality_stat, normality_p = stats.shapiro(clean_series)
        else:
            normality_stat, normality_p = None, None
        
        return {
            'mean': clean_series.mean(),
            'median': clean_series.median(),
            'std_dev': clean_series.std(),
            'skewness': skewness,
            'kurtosis': kurtosis,
            'normality_test_p_value': normality_p,
            'is_normal': normality_p > 0.05 if normality_p else None,
            'min': clean_series.min(),
            'max': clean_series.max(),
            'q25': clean_series.quantile(0.25),
            'q75': clean_series.quantile(0.75)
        }
    
    def hypothesis_test_comparison(self, group1: pd.Series, group2: pd.Series,
                                   test_type: str = 'ttest') -> Dict:
        """
        Perform hypothesis test comparing two groups
        
        Args:
            group1: First data series
            group2: Second data series
            test_type: Type of test ('ttest', 'mannwhitney', 'ks')
            
        Returns:
            Dictionary with test results and p-value
        """
        group1_clean = group1.dropna()
        group2_clean = group2.dropna()
        
        if test_type == 'ttest':
            statistic, p_value = stats.ttest_ind(group1_clean, group2_clean)
            test_name = "Independent T-Test"
        elif test_type == 'mannwhitney':
            statistic, p_value = stats.mannwhitneyu(group1_clean, group2_clean)
            test_name = "Mann-Whitney U Test"
        elif test_type == 'ks':
            statistic, p_value = stats.ks_2samp(group1_clean, group2_clean)
            test_name = "Kolmogorov-Smirnov Test"
        else:
            raise ValueError(f"Unknown test type: {test_type}")
        
        return {
            'test': test_name,
            'statistic': statistic,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'group1_mean': group1_clean.mean(),
            'group2_mean': group2_clean.mean(),
            'group1_count': len(group1_clean),
            'group2_count': len(group2_clean)
        }


class RiskAnalyzer:
    """Analyzes financial risk metrics"""
    
    def __init__(self, confidence_level: float = 0.95):
        """
        Initialize Risk Analyzer
        
        Args:
            confidence_level: Confidence level for VaR (default: 0.95 = 95%)
        """
        self.confidence_level = confidence_level
    
    def calculate_value_at_risk(self, returns: pd.Series) -> Dict:
        """
        Calculate Value at Risk (VaR) using percentile method
        
        Args:
            returns: Series of returns or price changes
            
        Returns:
            Dictionary with VaR metrics
        """
        clean_returns = returns.dropna()
        
        var_percentile = 1 - self.confidence_level
        var = clean_returns.quantile(var_percentile)
        
        # Expected Shortfall (CVaR)
        cvar = clean_returns[clean_returns <= var].mean()
        
        return {
            'confidence_level': self.confidence_level,
            'var': var,
            'conditional_var': cvar,
            'interpretation': f"Potential loss exceeds {abs(var):.4f} with {(1-self.confidence_level)*100:.0f}% probability"
        }
    
    def calculate_volatility(self, returns: pd.Series, window: int = 20) -> Dict:
        """
        Calculate volatility metrics
        
        Args:
            returns: Series of returns
            window: Rolling window size
            
        Returns:
            Dictionary with volatility statistics
        """
        clean_returns = returns.dropna()
        
        annual_volatility = clean_returns.std() * np.sqrt(252)  # 252 trading days
        rolling_vol = clean_returns.rolling(window=window).std()
        
        return {
            'daily_volatility': clean_returns.std(),
            'annual_volatility': annual_volatility,
            'current_volatility': rolling_vol.iloc[-1] if not rolling_vol.empty else None,
            'avg_volatility': rolling_vol.mean()
        }
    
    def calculate_sharpe_ratio(self, returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        """
        Calculate Sharpe Ratio for risk-adjusted returns
        
        Args:
            returns: Series of returns
            risk_free_rate: Annual risk-free rate (default: 2%)
            
        Returns:
            Sharpe Ratio value
        """
        clean_returns = returns.dropna()
        
        avg_return = clean_returns.mean() * 252
        volatility = clean_returns.std() * np.sqrt(252)
        
        sharpe_ratio = (avg_return - risk_free_rate) / volatility if volatility > 0 else 0
        
        return round(sharpe_ratio, 4)


class TrendAnalyzer:
    """Analyzes trends and seasonality in time series"""
    
    def __init__(self):
        """Initialize Trend Analyzer"""
        pass
    
    def detect_trend(self, series: pd.Series, window: int = 20) -> Dict:
        """
        Detect trend direction using moving average
        
        Args:
            series: Time series data
            window: Window size for moving average
            
        Returns:
            Dictionary with trend information
        """
        if len(series) < window:
            return {'trend': 'insufficient_data', 'strength': 0}
        
        sma = series.rolling(window=window).mean()
        last_value = series.iloc[-1]
        sma_value = sma.iloc[-1]
        
        trend = 'uptrend' if last_value > sma_value else 'downtrend' if last_value < sma_value else 'neutral'
        
        # Calculate trend strength
        recent_values = series.iloc[-window:]
        trend_strength = (recent_values - recent_values.mean()).std() / recent_values.mean() if recent_values.mean() != 0 else 0
        
        return {
            'trend': trend,
            'strength': round(trend_strength, 4),
            'current_value': last_value,
            'moving_average': sma_value
        }
    
    def detect_seasonality(self, series: pd.Series, periods: int = 12) -> Dict:
        """
        Detect seasonality patterns using autocorrelation
        
        Args:
            series: Time series data
            periods: Number of periods to check for seasonality
            
        Returns:
            Dictionary with seasonality detection results
        """
        if len(series) < periods:
            return {'has_seasonality': False, 'lags': []}
        
        clean_series = series.dropna()
        
        significant_lags = []
        for lag in range(1, min(periods + 1, len(clean_series) // 2)):
            # Calculate autocorrelation
            autocorr = clean_series.autocorr(lag)
            if abs(autocorr) > 0.3:  # Threshold for significance
                significant_lags.append({'lag': lag, 'autocorr': autocorr})
        
        return {
            'has_seasonality': len(significant_lags) > 0,
            'significant_lags': significant_lags,
            'strongest_lag': significant_lags[0] if significant_lags else None
        }
