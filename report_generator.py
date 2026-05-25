"""
Report Generator Module
Generates automated weekly and monthly financial reports with visualizations
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
from config import REPORT_CONFIG
from visualization_engine import VisualizationEngine
from kpi_calculator import KPICalculator


class ReportGenerator:
    """Generates automated financial summary reports"""
    
    def __init__(self, config: Dict = None):
        """Initialize Report Generator with configuration"""
        self.config = config or REPORT_CONFIG
        self.viz_engine = VisualizationEngine()
        self.kpi_calculator = KPICalculator()
        
        # Create output directory if it doesn't exist
        output_dir = self.config.get('output_directory', 'reports')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_weekly_report(self, df: pd.DataFrame, week_start_date: str = None,
                              revenue_column: str = 'revenue',
                              cost_column: str = 'cost',
                              date_column: str = 'date') -> Dict:
        """
        Generate weekly financial summary report
        
        Args:
            df: DataFrame with financial data
            week_start_date: Start date of the week (YYYY-MM-DD)
            revenue_column: Name of revenue column
            cost_column: Name of cost column
            date_column: Name of date column
            
        Returns:
            Dictionary with report path and status
        """
        try:
            # Determine week boundaries
            if week_start_date:
                week_start = pd.to_datetime(week_start_date)
            else:
                week_start = pd.Timestamp.now() - timedelta(days=7)
            
            week_end = week_start + timedelta(days=6)
            
            # Filter data for the week
            df_copy = df.copy()
            df_copy[date_column] = pd.to_datetime(df_copy[date_column])
            df_week = df_copy[(df_copy[date_column] >= week_start) & 
                             (df_copy[date_column] <= week_end)]
            
            if df_week.empty:
                return {
                    'status': 'failed',
                    'error': f'No data available for week starting {week_start.date()}'
                }
            
            # Calculate KPIs
            total_revenue = self.kpi_calculator.calculate_total_revenue(df_week, revenue_column)
            
            df_with_margin = self.kpi_calculator.calculate_profit_margin(df_week, revenue_column, cost_column)
            avg_margin = df_with_margin['profit_margin'].mean()
            
            # Calculate growth (compare to previous week)
            prev_week_start = week_start - timedelta(days=7)
            prev_week_end = week_start - timedelta(days=1)
            df_prev_week = df_copy[(df_copy[date_column] >= prev_week_start) & 
                                  (df_copy[date_column] <= prev_week_end)]
            
            if not df_prev_week.empty:
                prev_revenue = self.kpi_calculator.calculate_total_revenue(df_prev_week, revenue_column)
                growth_rate = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
            else:
                growth_rate = None
            
            # Create visualizations
            figures = []
            
            # Daily revenue trend
            daily_revenue = df_week.groupby(date_column)[revenue_column].sum().reset_index()
            fig1 = self.viz_engine.create_line_chart(
                daily_revenue, date_column, revenue_column,
                title=f"Daily Revenue - Week of {week_start.date()}",
                y_label="Revenue ($)"
            )
            figures.append(fig1)
            
            # Generate HTML report
            report_filename = f"weekly_report_{week_start.strftime('%Y%m%d')}.html"
            output_dir = self.config.get('output_directory', 'reports')
            report_path = os.path.join(output_dir, report_filename)
            
            # Add summary metrics to HTML
            summary_html = f"""
            <div style="background-color: white; padding: 20px; margin: 20px 0; border-radius: 8px;">
                <h2>Weekly Summary - {week_start.date()} to {week_end.date()}</h2>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr style="border-bottom: 1px solid #ddd;">
                        <td style="padding: 10px;"><strong>Total Revenue:</strong></td>
                        <td style="padding: 10px;">${total_revenue:,.2f}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #ddd;">
                        <td style="padding: 10px;"><strong>Average Profit Margin:</strong></td>
                        <td style="padding: 10px;">{avg_margin*100:.2f}%</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #ddd;">
                        <td style="padding: 10px;"><strong>Week-over-Week Growth:</strong></td>
                        <td style="padding: 10px;">{f"{growth_rate:.2f}%" if growth_rate is not None else "N/A"}</td>
                    </tr>
                </table>
            </div>
            """
            
            self.viz_engine.embed_in_html(
                figures, report_path,
                title=f"Weekly Financial Report - {week_start.date()}"
            )
            
            return {
                'status': 'success',
                'report_path': report_path,
                'metrics': {
                    'total_revenue': total_revenue,
                    'avg_profit_margin': avg_margin,
                    'growth_rate': growth_rate
                }
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def generate_monthly_report(self, df: pd.DataFrame, year: int = None, month: int = None,
                               revenue_column: str = 'revenue',
                               cost_column: str = 'cost',
                               date_column: str = 'date') -> Dict:
        """
        Generate monthly financial summary report
        
        Args:
            df: DataFrame with financial data
            year: Year for the report
            month: Month for the report (1-12)
            revenue_column: Name of revenue column
            cost_column: Name of cost column
            date_column: Name of date column
            
        Returns:
            Dictionary with report path and status
        """
        try:
            # Determine month boundaries
            if year and month:
                month_start = pd.Timestamp(year=year, month=month, day=1)
            else:
                now = pd.Timestamp.now()
                month_start = pd.Timestamp(year=now.year, month=now.month, day=1)
            
            # Calculate last day of month
            if month_start.month == 12:
                month_end = pd.Timestamp(year=month_start.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                month_end = pd.Timestamp(year=month_start.year, month=month_start.month + 1, day=1) - timedelta(days=1)
            
            # Filter data for the month
            df_copy = df.copy()
            df_copy[date_column] = pd.to_datetime(df_copy[date_column])
            df_month = df_copy[(df_copy[date_column] >= month_start) & 
                              (df_copy[date_column] <= month_end)]
            
            if df_month.empty:
                return {
                    'status': 'failed',
                    'error': f'No data available for {month_start.strftime("%B %Y")}'
                }
            
            # Calculate KPIs
            total_revenue = self.kpi_calculator.calculate_total_revenue(df_month, revenue_column)
            
            df_with_margin = self.kpi_calculator.calculate_profit_margin(df_month, revenue_column, cost_column)
            avg_margin = df_with_margin['profit_margin'].mean()
            
            # Calculate growth (compare to previous month)
            if month_start.month == 1:
                prev_month_start = pd.Timestamp(year=month_start.year - 1, month=12, day=1)
            else:
                prev_month_start = pd.Timestamp(year=month_start.year, month=month_start.month - 1, day=1)
            
            prev_month_end = month_start - timedelta(days=1)
            
            df_prev_month = df_copy[(df_copy[date_column] >= prev_month_start) & 
                                   (df_copy[date_column] <= prev_month_end)]
            
            if not df_prev_month.empty:
                prev_revenue = self.kpi_calculator.calculate_total_revenue(df_prev_month, revenue_column)
                growth_rate = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
            else:
                growth_rate = None
            
            # Create visualizations
            figures = []
            
            # Daily revenue trend
            daily_revenue = df_month.groupby(date_column)[revenue_column].sum().reset_index()
            fig1 = self.viz_engine.create_line_chart(
                daily_revenue, date_column, revenue_column,
                title=f"Daily Revenue - {month_start.strftime('%B %Y')}",
                y_label="Revenue ($)"
            )
            figures.append(fig1)
            
            # Generate HTML report
            report_filename = f"monthly_report_{month_start.strftime('%Y%m')}.html"
            output_dir = self.config.get('output_directory', 'reports')
            report_path = os.path.join(output_dir, report_filename)
            
            self.viz_engine.embed_in_html(
                figures, report_path,
                title=f"Monthly Financial Report - {month_start.strftime('%B %Y')}"
            )
            
            return {
                'status': 'success',
                'report_path': report_path,
                'metrics': {
                    'total_revenue': total_revenue,
                    'avg_profit_margin': avg_margin,
                    'growth_rate': growth_rate
                }
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
