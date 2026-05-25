"""
Financial Ratios & Metrics Module
Comprehensive financial ratio calculations and analysis
"""

import numpy as np
import pandas as pd


class FinancialRatios:
    """Calculate comprehensive financial ratios"""
    
    @staticmethod
    def profitability_ratios(revenue, net_income, gross_profit, total_assets, equity):
        """
        Calculate profitability ratios
        
        Args:
            revenue: Total revenue
            net_income: Net income
            gross_profit: Gross profit
            total_assets: Total assets
            equity: Shareholders equity
        
        Returns:
            Dictionary of profitability ratios
        """
        return {
            'Gross_Profit_Margin': (gross_profit / revenue * 100) if revenue > 0 else 0,
            'Net_Profit_Margin': (net_income / revenue * 100) if revenue > 0 else 0,
            'Return_on_Assets': (net_income / total_assets * 100) if total_assets > 0 else 0,
            'Return_on_Equity': (net_income / equity * 100) if equity > 0 else 0,
            'Return_on_Investment': (net_income / (total_assets + equity) * 100) if (total_assets + equity) > 0 else 0
        }
    
    @staticmethod
    def liquidity_ratios(current_assets, current_liabilities, inventory, cash):
        """
        Calculate liquidity ratios
        
        Args:
            current_assets: Current assets
            current_liabilities: Current liabilities
            inventory: Inventory value
            cash: Cash on hand
        
        Returns:
            Dictionary of liquidity ratios
        """
        quick_assets = current_assets - inventory
        
        return {
            'Current_Ratio': (current_assets / current_liabilities) if current_liabilities > 0 else float('inf'),
            'Quick_Ratio': (quick_assets / current_liabilities) if current_liabilities > 0 else float('inf'),
            'Cash_Ratio': (cash / current_liabilities) if current_liabilities > 0 else float('inf'),
            'Working_Capital': current_assets - current_liabilities,
            'Working_Capital_Ratio': ((current_assets - current_liabilities) / current_assets * 100) if current_assets > 0 else 0
        }
    
    @staticmethod
    def efficiency_ratios(revenue, total_assets, inventory, accounts_receivable, cogs):
        """
        Calculate efficiency/activity ratios
        
        Args:
            revenue: Total revenue
            total_assets: Total assets
            inventory: Inventory value
            accounts_receivable: AR balance
            cogs: Cost of goods sold
        
        Returns:
            Dictionary of efficiency ratios
        """
        return {
            'Asset_Turnover': (revenue / total_assets) if total_assets > 0 else 0,
            'Inventory_Turnover': (cogs / inventory) if inventory > 0 else 0,
            'Receivables_Turnover': (revenue / accounts_receivable) if accounts_receivable > 0 else 0,
            'Days_Inventory_Outstanding': (365 / ((cogs / inventory) if inventory > 0 else 1)),
            'Days_Sales_Outstanding': (365 / ((revenue / accounts_receivable) if accounts_receivable > 0 else 1))
        }
    
    @staticmethod
    def leverage_ratios(total_assets, total_liabilities, net_income, interest_expense, ebit):
        """
        Calculate leverage/solvency ratios
        
        Args:
            total_assets: Total assets
            total_liabilities: Total liabilities
            net_income: Net income
            interest_expense: Interest expense
            ebit: Earnings before interest and taxes
        
        Returns:
            Dictionary of leverage ratios
        """
        equity = total_assets - total_liabilities
        
        return {
            'Debt_to_Equity': (total_liabilities / equity) if equity > 0 else float('inf'),
            'Debt_to_Assets': (total_liabilities / total_assets) if total_assets > 0 else 0,
            'Equity_Ratio': (equity / total_assets * 100) if total_assets > 0 else 0,
            'Interest_Coverage': (ebit / interest_expense) if interest_expense > 0 else float('inf'),
            'Debt_Service_Coverage': ((net_income + interest_expense) / interest_expense) if interest_expense > 0 else float('inf')
        }
    
    @staticmethod
    def market_ratios(net_income, number_of_shares, market_price_per_share, earnings, 
                     book_value_per_share, dividend_per_share=0):
        """
        Calculate market-related ratios
        
        Args:
            net_income: Net income
            number_of_shares: Number of shares outstanding
            market_price_per_share: Market price per share
            earnings: Total earnings
            book_value_per_share: Book value per share
            dividend_per_share: Dividend per share
        
        Returns:
            Dictionary of market ratios
        """
        eps = net_income / number_of_shares if number_of_shares > 0 else 0
        market_cap = market_price_per_share * number_of_shares
        
        return {
            'EPS': eps,
            'PE_Ratio': (market_price_per_share / eps) if eps > 0 else float('inf'),
            'PB_Ratio': (market_price_per_share / book_value_per_share) if book_value_per_share > 0 else float('inf'),
            'Market_Cap': market_cap,
            'Dividend_Yield': (dividend_per_share / market_price_per_share * 100) if market_price_per_share > 0 else 0,
            'Payout_Ratio': (dividend_per_share / eps * 100) if eps > 0 else 0
        }


class MetricsAnalyzer:
    """Analyze and interpret financial metrics"""
    
    @staticmethod
    def calculate_metrics_from_transactions(df, revenue_col='amount', cost_col=None, 
                                          quantity_col=None, customer_col='customer_id',
                                          date_col='date'):
        """
        Calculate key metrics from transaction data
        
        Args:
            df: Transaction dataframe
            revenue_col: Revenue column
            cost_col: Cost column (if available)
            quantity_col: Quantity column (if available)
            customer_col: Customer column
            date_col: Date column
        
        Returns:
            Dictionary of calculated metrics
        """
        total_revenue = df[revenue_col].sum()
        total_cost = df[cost_col].sum() if cost_col and cost_col in df.columns else total_revenue * 0.6
        
        n_transactions = len(df)
        n_customers = df[customer_col].nunique()
        n_days = (pd.to_datetime(df[date_col]).max() - pd.to_datetime(df[date_col]).min()).days + 1
        
        metrics = {
            'Total_Revenue': total_revenue,
            'Total_Cost': total_cost,
            'Gross_Profit': total_revenue - total_cost,
            'Gross_Margin_%': ((total_revenue - total_cost) / total_revenue * 100) if total_revenue > 0 else 0,
            'Number_Transactions': n_transactions,
            'Number_Customers': n_customers,
            'Days_Period': n_days,
            'Avg_Transaction_Value': total_revenue / n_transactions if n_transactions > 0 else 0,
            'Avg_Customer_Value': total_revenue / n_customers if n_customers > 0 else 0,
            'Revenue_Per_Day': total_revenue / n_days if n_days > 0 else 0,
            'Revenue_Per_Customer_Per_Day': total_revenue / (n_customers * n_days) if n_customers * n_days > 0 else 0,
            'Customer_Acquisition_Cost': total_cost / n_customers if n_customers > 0 else 0,
            'Repeat_Purchase_Rate': ((n_transactions - n_customers) / n_customers * 100) if n_customers > 0 else 0
        }
        
        return metrics
    
    @staticmethod
    def segment_metrics(df, revenue_col='amount', segment_col='category', 
                       cost_col=None, customer_col='customer_id'):
        """
        Calculate metrics by segment
        
        Args:
            df: Transaction dataframe
            revenue_col: Revenue column
            segment_col: Segment column
            cost_col: Cost column
            customer_col: Customer column
        
        Returns:
            Segment metrics dataframe
        """
        segment_metrics = []
        
        for segment in df[segment_col].unique():
            segment_data = df[df[segment_col] == segment]
            
            revenue = segment_data[revenue_col].sum()
            cost = segment_data[cost_col].sum() if cost_col and cost_col in df.columns else revenue * 0.6
            
            metrics = {
                'Segment': segment,
                'Revenue': revenue,
                'Cost': cost,
                'Profit': revenue - cost,
                'Margin_%': ((revenue - cost) / revenue * 100) if revenue > 0 else 0,
                'Transactions': len(segment_data),
                'Customers': segment_data[customer_col].nunique(),
                'Avg_Transaction_Value': revenue / len(segment_data) if len(segment_data) > 0 else 0,
                'Market_Share_%': (revenue / df[revenue_col].sum() * 100) if df[revenue_col].sum() > 0 else 0
            }
            
            segment_metrics.append(metrics)
        
        return pd.DataFrame(segment_metrics).sort_values('Profit', ascending=False)
    
    @staticmethod
    def performance_comparison(current_metrics, previous_metrics):
        """
        Compare current vs previous metrics
        
        Args:
            current_metrics: Current period metrics dict
            previous_metrics: Previous period metrics dict
        
        Returns:
            Comparison with variance
        """
        comparison = []
        
        for metric in current_metrics:
            if metric in previous_metrics:
                current = current_metrics[metric]
                previous = previous_metrics[metric]
                
                if isinstance(current, (int, float)) and isinstance(previous, (int, float)):
                    variance = current - previous
                    variance_pct = (variance / previous * 100) if previous != 0 else 0
                    
                    comparison.append({
                        'Metric': metric,
                        'Previous': previous,
                        'Current': current,
                        'Variance': variance,
                        'Variance_%': round(variance_pct, 2),
                        'Trend': 'UP' if variance > 0 else ('DOWN' if variance < 0 else 'FLAT')
                    })
        
        return pd.DataFrame(comparison).sort_values('Variance_%', ascending=False)


class KPITracker:
    """Track and monitor KPIs"""
    
    @staticmethod
    def initialize_kpi_dashboard(metrics_dict):
        """
        Create KPI dashboard structure
        
        Args:
            metrics_dict: Dictionary of metrics
        
        Returns:
            KPI dashboard structure
        """
        dashboard = {
            'timestamp': pd.Timestamp.now(),
            'metrics': metrics_dict,
            'alerts': [],
            'trends': {}
        }
        
        return dashboard
    
    @staticmethod
    def evaluate_kpi_against_target(actual, target, tolerance_pct=5):
        """
        Evaluate KPI performance against target
        
        Args:
            actual: Actual value
            target: Target value
            tolerance_pct: Acceptable variance percentage
        
        Returns:
            KPI status and evaluation
        """
        variance = actual - target
        variance_pct = (variance / target * 100) if target != 0 else 0
        
        if variance_pct >= tolerance_pct:
            status = 'EXCEEDED'
            health = 'EXCELLENT'
        elif variance_pct >= -tolerance_pct:
            status = 'ON_TARGET'
            health = 'GOOD'
        elif variance_pct >= -2 * tolerance_pct:
            status = 'BELOW_TARGET'
            health = 'WARNING'
        else:
            status = 'CRITICAL'
            health = 'POOR'
        
        return {
            'actual': actual,
            'target': target,
            'variance': variance,
            'variance_pct': round(variance_pct, 2),
            'status': status,
            'health': health
        }
    
    @staticmethod
    def generate_kpi_report(metrics, targets, previous_metrics=None):
        """
        Generate comprehensive KPI report
        
        Args:
            metrics: Current metrics dictionary
            targets: Target dictionary
            previous_metrics: Previous period metrics
        
        Returns:
            Comprehensive KPI report
        """
        report = {
            'current_metrics': metrics,
            'target_metrics': targets,
            'kpi_evaluations': {},
            'trends': {},
            'alerts': [],
            'summary': {}
        }
        
        # Evaluate each KPI
        for metric, target_value in targets.items():
            if metric in metrics:
                actual_value = metrics[metric]
                evaluation = KPITracker.evaluate_kpi_against_target(actual_value, target_value)
                report['kpi_evaluations'][metric] = evaluation
                
                # Add alert if poor health
                if evaluation['health'] in ['WARNING', 'POOR']:
                    report['alerts'].append({
                        'kpi': metric,
                        'status': evaluation['health'],
                        'message': f"{metric} is {evaluation['status']}: {evaluation['variance_pct']}% vs target"
                    })
        
        # Summary
        total_kpis = len(report['kpi_evaluations'])
        excellent_count = sum(1 for e in report['kpi_evaluations'].values() if e['health'] == 'EXCELLENT')
        warning_count = sum(1 for e in report['kpi_evaluations'].values() if e['health'] in ['WARNING', 'POOR'])
        
        report['summary'] = {
            'total_kpis': total_kpis,
            'excellent': excellent_count,
            'good': total_kpis - excellent_count - warning_count,
            'warning': warning_count,
            'overall_health': 'EXCELLENT' if warning_count == 0 else ('GOOD' if warning_count <= 2 else 'POOR')
        }
        
        return report
