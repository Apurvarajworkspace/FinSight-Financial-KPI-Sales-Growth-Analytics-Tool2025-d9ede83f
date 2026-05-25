"""
Advanced Visualization Module
Creates interactive dashboards, performance tracking, and alert visualizations
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from typing import List, Dict, Optional
import os


class DashboardBuilder:
    """Builds interactive financial dashboards"""
    
    def __init__(self, config: Dict = None):
        """Initialize Dashboard Builder"""
        self.config = config or {}
    
    def create_kpi_dashboard(self, kpi_data: Dict[str, float], 
                            previous_kpi_data: Dict[str, float] = None,
                            title: str = "Financial KPI Dashboard") -> go.Figure:
        """
        Create a KPI summary dashboard with indicators
        
        Args:
            kpi_data: Dictionary of current KPIs
            previous_kpi_data: Dictionary of previous period KPIs for comparison
            title: Dashboard title
            
        Returns:
            Plotly Figure object
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=list(kpi_data.keys()),
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]]
        )
        
        kpi_names = list(kpi_data.keys())
        positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
        
        for i, (kpi_name, value) in enumerate(kpi_data.items()):
            if i >= 4:
                break
            
            delta = None
            if previous_kpi_data and kpi_name in previous_kpi_data:
                prev_value = previous_kpi_data[kpi_name]
                delta = value - prev_value
            
            row, col = positions[i]
            
            fig.add_trace(
                go.Indicator(
                    mode="number+delta" if delta is not None else "number",
                    value=value,
                    title=kpi_name,
                    delta={'reference': previous_kpi_data[kpi_name]} if delta is not None else None,
                    number={'prefix': "$" if 'revenue' in kpi_name.lower() or 'profit' in kpi_name.lower() else ""},
                    domain={'x': [0, 1], 'y': [0, 1]}
                ),
                row=row, col=col
            )
        
        fig.update_layout(
            title=title,
            height=600,
            width=1000,
            showlegend=False
        )
        
        return fig
    
    def create_performance_gauge(self, current_value: float, target_value: float,
                                metric_name: str = "Performance", min_value: float = 0,
                                max_value: float = 100) -> go.Figure:
        """
        Create a gauge chart for performance tracking
        
        Args:
            current_value: Current metric value
            target_value: Target metric value
            metric_name: Name of the metric
            min_value: Minimum gauge value
            max_value: Maximum gauge value
            
        Returns:
            Plotly Figure object
        """
        fig = go.Figure(data=[go.Gauge(
            mode="gauge+number+delta",
            value=current_value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title=metric_name,
            delta={'reference': target_value},
            gauge={
                'axis': {'range': [min_value, max_value]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [min_value, max_value * 0.33], 'color': "lightgray"},
                    {'range': [max_value * 0.33, max_value * 0.67], 'color': "gray"},
                    {'range': [max_value * 0.67, max_value], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': target_value
                }
            }
        )])
        
        fig.update_layout(height=500, width=500)
        return fig
    
    def create_heatmap(self, df: pd.DataFrame, title: str = "Metric Correlation Heatmap") -> go.Figure:
        """
        Create a correlation heatmap
        
        Args:
            df: DataFrame with numeric data
            title: Chart title
            
        Returns:
            Plotly Figure object
        """
        numeric_df = df.select_dtypes(include=['number'])
        correlation = numeric_df.corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=correlation.values,
            x=correlation.columns,
            y=correlation.columns,
            colorscale='RdYlGn',
            zmid=0,
            zmin=-1,
            zmax=1,
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title=title,
            height=600,
            width=800,
            xaxis_title="Metrics",
            yaxis_title="Metrics"
        )
        
        return fig
    
    def create_waterfall_chart(self, categories: List[str], values: List[float],
                              title: str = "Waterfall Analysis") -> go.Figure:
        """
        Create a waterfall chart showing cumulative impact
        
        Args:
            categories: List of category names
            values: List of values
            title: Chart title
            
        Returns:
            Plotly Figure object
        """
        fig = go.Figure(go.Waterfall(
            name="Amount",
            orientation="v",
            x=categories,
            textposition="outside",
            y=values,
            connector={"line": {"color": "rgba(63, 63, 63, 0.5)"}},
            increasing={"marker": {"color": "green"}},
            decreasing={"marker": {"color": "red"}},
            totals={"marker": {"color": "blue"}}
        ))
        
        fig.update_layout(
            title=title,
            height=600,
            width=1000,
            yaxis_title="Amount ($)",
            xaxis_title="Categories"
        )
        
        return fig


class AlertManager:
    """Manages alerts and threshold monitoring"""
    
    def __init__(self):
        """Initialize Alert Manager"""
        self.alerts = []
    
    def create_threshold_alert(self, metric_name: str, current_value: float,
                              threshold: float, condition: str = 'below',
                              severity: str = 'warning') -> Optional[Dict]:
        """
        Create an alert if threshold is breached
        
        Args:
            metric_name: Name of the metric
            current_value: Current metric value
            threshold: Alert threshold value
            condition: 'below' or 'above'
            severity: 'info', 'warning', 'critical'
            
        Returns:
            Alert dictionary if triggered, None otherwise
        """
        triggered = False
        
        if condition == 'below' and current_value < threshold:
            triggered = True
        elif condition == 'above' and current_value > threshold:
            triggered = True
        
        if triggered:
            alert = {
                'metric': metric_name,
                'current_value': current_value,
                'threshold': threshold,
                'condition': condition,
                'severity': severity,
                'timestamp': pd.Timestamp.now(),
                'message': f"{severity.upper()}: {metric_name} is {current_value:.2f} ({condition} threshold of {threshold:.2f})"
            }
            self.alerts.append(alert)
            return alert
        
        return None
    
    def create_anomaly_alert(self, metric_name: str, anomaly_count: int,
                            anomaly_severity: str = 'warning') -> Optional[Dict]:
        """
        Create alert for detected anomalies
        
        Args:
            metric_name: Name of the metric
            anomaly_count: Number of anomalies detected
            anomaly_severity: Severity level of anomalies
            
        Returns:
            Alert dictionary if anomalies found, None otherwise
        """
        if anomaly_count > 0:
            alert = {
                'metric': metric_name,
                'anomaly_count': anomaly_count,
                'severity': anomaly_severity,
                'timestamp': pd.Timestamp.now(),
                'message': f"{anomaly_severity.upper()}: Detected {anomaly_count} anomalies in {metric_name}"
            }
            self.alerts.append(alert)
            return alert
        
        return None
    
    def get_active_alerts(self) -> pd.DataFrame:
        """
        Get all active alerts as DataFrame
        
        Returns:
            DataFrame with alert information
        """
        if not self.alerts:
            return pd.DataFrame()
        
        return pd.DataFrame(self.alerts)
    
    def clear_alerts(self):
        """Clear all stored alerts"""
        self.alerts = []


class ReportComposer:
    """Composes advanced analytical reports"""
    
    def __init__(self):
        """Initialize Report Composer"""
        pass
    
    def create_html_report(self, figures: List[go.Figure], alerts: List[Dict],
                          analysis_summary: Dict, output_path: str = "advanced_report.html") -> str:
        """
        Create comprehensive HTML report with all analyses
        
        Args:
            figures: List of Plotly figures
            alerts: List of alert dictionaries
            analysis_summary: Summary of analysis results
            output_path: Output file path
            
        Returns:
            Path to generated report
        """
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Advanced Financial Analytics Report</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }
                .container {
                    max-width: 1400px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    overflow: hidden;
                }
                .header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }
                .header h1 {
                    margin: 0;
                    font-size: 2.5em;
                }
                .header p {
                    margin: 10px 0 0 0;
                    opacity: 0.9;
                }
                .content {
                    padding: 30px;
                }
                .alerts-section {
                    margin-bottom: 30px;
                    padding: 20px;
                    border-left: 4px solid #ff6b6b;
                    background-color: #fff5f5;
                    border-radius: 5px;
                }
                .alerts-section h3 {
                    margin-top: 0;
                    color: #c92a2a;
                }
                .alert-item {
                    padding: 10px;
                    margin: 5px 0;
                    background: white;
                    border-radius: 3px;
                    border-left: 3px solid #ff8787;
                }
                .alert-item.critical {
                    border-left-color: #e03131;
                    background-color: #ffe0e0;
                }
                .alert-item.warning {
                    border-left-color: #fd7e14;
                    background-color: #fff3e0;
                }
                .chart-container {
                    margin: 30px 0;
                    padding: 20px;
                    background: #f8f9fa;
                    border-radius: 8px;
                }
                .summary-section {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    margin: 30px 0;
                }
                .summary-card {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                }
                .summary-card h4 {
                    margin: 0 0 10px 0;
                    font-size: 1.1em;
                    opacity: 0.9;
                }
                .summary-card p {
                    margin: 0;
                    font-size: 1.8em;
                    font-weight: bold;
                }
                .footer {
                    background: #f8f9fa;
                    padding: 20px;
                    text-align: center;
                    color: #666;
                    border-top: 1px solid #dee2e6;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Advanced Financial Analytics Report</h1>
                    <p>Comprehensive Analysis and Insights</p>
                </div>
                
                <div class="content">
        """
        
        # Add alerts section
        if alerts:
            html_content += '<div class="alerts-section"><h3>⚠️ Active Alerts</h3>'
            for alert in alerts:
                severity_class = alert.get('severity', 'warning').lower()
                html_content += f'<div class="alert-item {severity_class}"><strong>{alert.get("message", "Alert")}</strong></div>'
            html_content += '</div>'
        
        # Add summary section
        if analysis_summary:
            html_content += '<div class="summary-section">'
            for key, value in analysis_summary.items():
                html_content += f'''
                <div class="summary-card">
                    <h4>{key}</h4>
                    <p>{value if isinstance(value, str) else f"{value:.2f}" if isinstance(value, (int, float)) else value}</p>
                </div>
                '''
            html_content += '</div>'
        
        # Add figures
        for i, fig in enumerate(figures):
            html_content += f'<div class="chart-container">{fig.to_html(include_plotlyjs=False, div_id=f"chart_{i}")}</div>'
        
        html_content += """
                </div>
                
                <div class="footer">
                    <p>Generated on {}  | Advanced Analytics System</p>
                </div>
            </div>
        </body>
        </html>
        """.format(pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
