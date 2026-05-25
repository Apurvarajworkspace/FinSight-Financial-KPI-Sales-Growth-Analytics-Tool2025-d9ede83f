"""
Performance Attribution & Variance Analysis Module
Analyze contribution of different factors to overall performance
"""

import numpy as np
import pandas as pd


class PerformanceAttributor:
    """Analyze what drives financial performance"""
    
    @staticmethod
    def contribution_analysis(df, revenue_col='amount', segment_col='category', 
                             customer_col='customer_id', date_col='date'):
        """
        Analyze contribution by different dimensions
        
        Args:
            df: Transaction dataframe
            revenue_col: Revenue column
            segment_col: Segment/category column
            customer_col: Customer column
            date_col: Date column
        
        Returns:
            Contribution analysis
        """
        total_revenue = df[revenue_col].sum()
        
        # By segment/category
        segment_contrib = df.groupby(segment_col)[revenue_col].agg(['sum', 'count', 'mean'])
        segment_contrib['% of Total'] = (segment_contrib['sum'] / total_revenue * 100).round(2)
        segment_contrib.columns = ['Revenue', 'Transactions', 'Avg_Transaction', '% of Total']
        
        # By customer
        customer_contrib = df.groupby(customer_col)[revenue_col].sum().sort_values(ascending=False)
        top_customers_pct = (customer_contrib.head(10).sum() / total_revenue * 100)
        
        # By time period
        df_copy = df.copy()
        df_copy['date'] = pd.to_datetime(df_copy[date_col])
        df_copy['month'] = df_copy['date'].dt.to_period('M')
        
        monthly_contrib = df_copy.groupby('month')[revenue_col].agg(['sum', 'count', 'mean'])
        monthly_contrib.columns = ['Revenue', 'Transactions', 'Avg_Transaction']
        monthly_contrib['% of Total'] = (monthly_contrib['Revenue'] / total_revenue * 100).round(2)
        
        return {
            'total_revenue': total_revenue,
            'by_segment': segment_contrib,
            'top_customers_pct': top_customers_pct,
            'by_period': monthly_contrib,
            'segment_breakdown': segment_contrib['% of Total'].to_dict()
        }
    
    @staticmethod
    def waterfall_analysis(current_period, previous_period, label='Revenue'):
        """
        Create waterfall analysis showing changes
        
        Args:
            current_period: Current period value
            previous_period: Previous period value
            label: Label for analysis
        
        Returns:
            Waterfall components
        """
        change = current_period - previous_period
        pct_change = (change / abs(previous_period)) * 100 if previous_period != 0 else 0
        
        return {
            'previous_value': previous_period,
            'change': change,
            'change_pct': round(pct_change, 2),
            'current_value': current_period,
            'label': label,
            'direction': 'UP' if change > 0 else ('DOWN' if change < 0 else 'FLAT')
        }
    
    @staticmethod
    def variance_analysis(df, revenue_col='amount', budget_col=None, actual_col=None,
                         segment_col='category', category_col='category'):
        """
        Analyze variance between budget and actual
        
        Args:
            df: Transaction dataframe
            revenue_col: Actual revenue column
            budget_col: Budget values per segment
            segment_col: Segment column
        
        Returns:
            Variance analysis
        """
        if budget_col is None:
            # Create sample budget (assume budget is 90% of historical average)
            budget_col = {}
            for segment in df[segment_col].unique():
                segment_data = df[df[segment_col] == segment]
                budget_col[segment] = segment_data[revenue_col].sum() * 1.1  # 10% growth target
        
        # Actual by segment
        actual_by_segment = df.groupby(segment_col)[revenue_col].sum()
        
        # Calculate variance
        variance_analysis = []
        for segment in actual_by_segment.index:
            actual = actual_by_segment[segment]
            budget = budget_col.get(segment, actual)
            variance = actual - budget
            variance_pct = (variance / budget * 100) if budget != 0 else 0
            
            variance_analysis.append({
                'Segment': segment,
                'Budget': budget,
                'Actual': actual,
                'Variance': variance,
                'Variance_Pct': round(variance_pct, 2),
                'Status': 'FAVORABLE' if variance > 0 else ('UNFAVORABLE' if variance < 0 else 'ON_TRACK')
            })
        
        return pd.DataFrame(variance_analysis).sort_values('Variance', ascending=False)
    
    @staticmethod
    def driver_analysis(df, revenue_col='amount', drivers=['category', 'region']):
        """
        Multi-dimensional driver analysis
        
        Args:
            df: Transaction dataframe
            revenue_col: Revenue column
            drivers: Columns to analyze as drivers
        
        Returns:
            Impact of each driver on revenue
        """
        total_revenue = df[revenue_col].sum()
        driver_impacts = {}
        
        for driver in drivers:
            if driver in df.columns:
                impact = df.groupby(driver)[revenue_col].agg(['sum', 'mean', 'count'])
                impact.columns = ['Total_Revenue', 'Avg_Revenue', 'Count']
                impact['Revenue_Impact_%'] = (impact['Total_Revenue'] / total_revenue * 100).round(2)
                impact = impact.sort_values('Total_Revenue', ascending=False)
                driver_impacts[driver] = impact
        
        return driver_impacts


class VarianceExplainer:
    """Explain variance between periods"""
    
    @staticmethod
    def calculate_revenue_bridge(period1_data, period2_data, metric='amount'):
        """
        Calculate revenue bridge (what changed)
        
        Args:
            period1_data: Period 1 dataframe
            period2_data: Period 2 dataframe
            metric: Metric column
        
        Returns:
            Bridge components
        """
        total_p1 = period1_data[metric].sum()
        total_p2 = period2_data[metric].sum()
        
        # Volume effect (more/fewer transactions)
        volume_p1 = len(period1_data)
        volume_p2 = len(period2_data)
        volume_change = volume_p2 - volume_p1
        
        # Price/Mix effect (higher/lower average value)
        avg_p1 = period1_data[metric].mean()
        avg_p2 = period2_data[metric].mean()
        
        # Decompose change
        volume_impact = volume_change * avg_p1
        mix_impact = volume_p2 * (avg_p2 - avg_p1)
        
        total_change = total_p2 - total_p1
        
        return {
            'total_change': total_change,
            'volume_impact': volume_impact,
            'mix_impact': mix_impact,
            'bridge_sum': volume_impact + mix_impact,
            'bridge_accuracy': round((volume_impact + mix_impact) / total_change * 100, 1) if total_change != 0 else 0,
            'volume_pct': round(volume_impact / total_change * 100, 1) if total_change != 0 else 0,
            'mix_pct': round(mix_impact / total_change * 100, 1) if total_change != 0 else 0
        }
    
    @staticmethod
    def segment_performance_bridge(df, period1_dates, period2_dates, revenue_col='amount', 
                                  segment_col='category', date_col='date'):
        """
        Analyze performance change by segment
        
        Args:
            df: Transaction dataframe
            period1_dates: (start, end) for period 1
            period2_dates: (start, end) for period 2
            revenue_col: Revenue column
            segment_col: Segment column
            date_col: Date column
        
        Returns:
            Segment-level performance bridge
        """
        df_copy = df.copy()
        df_copy[date_col] = pd.to_datetime(df_copy[date_col])
        
        # Filter periods
        p1_start, p1_end = period1_dates
        p2_start, p2_end = period2_dates
        
        p1_data = df_copy[(df_copy[date_col] >= p1_start) & (df_copy[date_col] <= p1_end)]
        p2_data = df_copy[(df_copy[date_col] >= p2_start) & (df_copy[date_col] <= p2_end)]
        
        # By segment
        bridge = []
        for segment in df_copy[segment_col].unique():
            p1_segment = p1_data[p1_data[segment_col] == segment]
            p2_segment = p2_data[p2_data[segment_col] == segment]
            
            p1_revenue = p1_segment[revenue_col].sum()
            p2_revenue = p2_segment[revenue_col].sum()
            change = p2_revenue - p1_revenue
            
            bridge.append({
                'Segment': segment,
                'Period1_Revenue': p1_revenue,
                'Period2_Revenue': p2_revenue,
                'Revenue_Change': change,
                'Change_Pct': round((change / p1_revenue * 100), 2) if p1_revenue > 0 else 0
            })
        
        return pd.DataFrame(bridge).sort_values('Revenue_Change', ascending=False)


class PerformanceBenchmarking:
    """Benchmark performance against targets and historical"""
    
    @staticmethod
    def calculate_performance_metrics(data, targets=None):
        """
        Calculate performance against targets
        
        Args:
            data: Dictionary of actual values
            targets: Dictionary of target values
        
        Returns:
            Performance metrics
        """
        performance = []
        
        for metric, actual in data.items():
            target = targets.get(metric, actual * 1.1) if targets else actual * 1.1
            variance = actual - target
            variance_pct = (variance / target * 100) if target != 0 else 0
            
            performance.append({
                'Metric': metric,
                'Target': target,
                'Actual': actual,
                'Variance': variance,
                'Variance_Pct': round(variance_pct, 2),
                'Status': 'ACHIEVED' if variance >= 0 else 'MISSED'
            })
        
        return pd.DataFrame(performance).sort_values('Variance_Pct', ascending=False)
    
    @staticmethod
    def trend_vs_target(historical_data, target_value, metric_name='Metric'):
        """
        Analyze trend vs target
        
        Args:
            historical_data: List of historical values
            target_value: Target to achieve
            metric_name: Name of metric
        
        Returns:
            Trend analysis
        """
        data = np.array(historical_data)
        trend = np.polyfit(np.arange(len(data)), data, 1)[0]
        current = data[-1] if len(data) > 0 else 0
        avg = np.mean(data)
        
        gap_to_target = target_value - current
        periods_to_target = gap_to_target / trend if trend != 0 else float('inf')
        
        return {
            'metric_name': metric_name,
            'current_value': current,
            'target_value': target_value,
            'gap': gap_to_target,
            'average_value': avg,
            'trend': round(trend, 4),
            'periods_to_target': round(periods_to_target, 1) if periods_to_target != float('inf') else 'N/A',
            'on_track': gap_to_target <= 0 or trend > 0
        }
