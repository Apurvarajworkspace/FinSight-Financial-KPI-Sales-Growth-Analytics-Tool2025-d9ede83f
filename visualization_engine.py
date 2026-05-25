"""
Visualization Engine Module
Creates interactive visualizations with Plotly and statistical charts with Seaborn
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Dict, List, Optional
from config import VIZ_CONFIG
import os


class VisualizationEngine:
    """Creates interactive and statistical visualizations"""
    
    def __init__(self, config: Dict = None):
        """Initialize Visualization Engine with configuration"""
        self.config = config or VIZ_CONFIG
        sns.set_theme(style="whitegrid")
    
    def create_line_chart(self, df: pd.DataFrame, x_column: str, y_column: str,
                         title: str = "Time Series Trend",
                         x_label: str = None, y_label: str = None) -> go.Figure:
        """
        Create interactive line chart for time-series trends
        
        Args:
            df: DataFrame with data
            x_column: Column for x-axis (typically date)
            y_column: Column for y-axis (numeric values)
            title: Chart title
            x_label: X-axis label
            y_label: Y-axis label
            
        Returns:
            Plotly Figure object
            
        Raises:
            ValueError: If data is invalid
        """
        if df.empty:
            raise ValueError("Cannot create visualization: DataFrame is empty")
        
        if x_column not in df.columns or y_column not in df.columns:
            raise ValueError(f"Required columns not found in DataFrame")
        
        # Validate minimum data points
        if len(df) < 2:
            raise ValueError(f"Minimum 2 data points required for line chart, got {len(df)}")
        
        # Validate numeric data
        if not pd.api.types.is_numeric_dtype(df[y_column]):
            raise ValueError(f"Y-axis column '{y_column}' must contain numeric values")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df[x_column],
            y=df[y_column],
            mode='lines+markers',
            name=y_column,
            hovertemplate='<b>%{x}</b><br>Value: %{y:,.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x_label or x_column,
            yaxis_title=y_label or y_column,
            height=self.config.get('chart_height', 600),
            width=self.config.get('chart_width', 1000),
            hovermode='x unified'
        )
        
        return fig
    
    def create_bar_chart(self, df: pd.DataFrame, x_column: str, y_column: str,
                        title: str = "Categorical Comparison",
                        x_label: str = None, y_label: str = None,
                        orientation: str = 'v') -> go.Figure:
        """
        Create interactive bar chart for categorical comparisons
        
        Args:
            df: DataFrame with data
            x_column: Column for categories
            y_column: Column for numeric values
            title: Chart title
            x_label: X-axis label
            y_label: Y-axis label
            orientation: 'v' for vertical, 'h' for horizontal
            
        Returns:
            Plotly Figure object
            
        Raises:
            ValueError: If data is invalid
        """
        if df.empty:
            raise ValueError("Cannot create visualization: DataFrame is empty")
        
        if x_column not in df.columns or y_column not in df.columns:
            raise ValueError(f"Required columns not found in DataFrame")
        
        # Validate minimum data points
        if len(df) < 2:
            raise ValueError(f"Minimum 2 data points required for bar chart, got {len(df)}")
        
        # Validate numeric data
        if not pd.api.types.is_numeric_dtype(df[y_column]):
            raise ValueError(f"Y-axis column '{y_column}' must contain numeric values")
        
        # Limit categories
        max_categories = self.config.get('max_categories', 50)
        if len(df) > max_categories:
            raise ValueError(f"Too many categories: maximum {max_categories} allowed, got {len(df)}")
        
        fig = go.Figure()
        
        if orientation == 'v':
            fig.add_trace(go.Bar(
                x=df[x_column],
                y=df[y_column],
                hovertemplate='<b>%{x}</b><br>Value: %{y:,.2f}<extra></extra>'
            ))
        else:
            fig.add_trace(go.Bar(
                x=df[y_column],
                y=df[x_column],
                orientation='h',
                hovertemplate='<b>%{y}</b><br>Value: %{x:,.2f}<extra></extra>'
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x_label or x_column,
            yaxis_title=y_label or y_column,
            height=self.config.get('chart_height', 600),
            width=self.config.get('chart_width', 1000)
        )
        
        return fig
    
    def create_multi_line_chart(self, df: pd.DataFrame, x_column: str,
                               y_columns: List[str], title: str = "Multi-Series Comparison") -> go.Figure:
        """
        Create line chart with multiple series
        
        Args:
            df: DataFrame with data
            x_column: Column for x-axis
            y_columns: List of columns for y-axis
            title: Chart title
            
        Returns:
            Plotly Figure object
        """
        if df.empty:
            raise ValueError("Cannot create visualization: DataFrame is empty")
        
        fig = go.Figure()
        
        for y_col in y_columns:
            if y_col not in df.columns:
                raise ValueError(f"Column '{y_col}' not found")
            
            fig.add_trace(go.Scatter(
                x=df[x_column],
                y=df[y_col],
                mode='lines+markers',
                name=y_col,
                hovertemplate=f'<b>{y_col}</b><br>%{{x}}<br>Value: %{{y:,.2f}}<extra></extra>'
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x_column,
            yaxis_title="Value",
            height=self.config.get('chart_height', 600),
            width=self.config.get('chart_width', 1000),
            hovermode='x unified'
        )
        
        return fig
    
    def embed_in_html(self, figures: List[go.Figure], output_path: str,
                     title: str = "Financial Analytics Report") -> str:
        """
        Embed Plotly visualizations into HTML file
        
        Args:
            figures: List of Plotly figures
            output_path: Path to save HTML file
            title: Report title
            
        Returns:
            Path to created HTML file
        """
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                h1 {{
                    color: #333;
                    text-align: center;
                }}
                .chart-container {{
                    background-color: white;
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
        """
        
        for i, fig in enumerate(figures):
            html_content += f'<div class="chart-container" id="chart{i}"></div>\n'
            html_content += f'<script>\n'
            html_content += f'var data{i} = {fig.to_json()};\n'
            html_content += f'Plotly.newPlot("chart{i}", data{i}.data, data{i}.layout);\n'
            html_content += f'</script>\n'
        
        html_content += """
        </body>
        </html>
        """
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def create_heatmap(self, df: pd.DataFrame, title: str = "Correlation Heatmap",
                      output_path: str = None, annot: bool = True) -> str:
        """
        Create heatmap using Seaborn
        
        Args:
            df: DataFrame with numeric data (typically correlation matrix)
            title: Chart title
            output_path: Path to save image file
            annot: Whether to annotate cells with values
            
        Returns:
            Path to saved image file
            
        Raises:
            ValueError: If data contains non-numeric values
        """
        if df.empty:
            raise ValueError("Cannot create visualization: DataFrame is empty")
        
        # Validate numeric data
        non_numeric_cols = df.select_dtypes(exclude=['number']).columns.tolist()
        if non_numeric_cols:
            raise ValueError(f"Heatmap requires numeric data. Non-numeric columns found: {', '.join(non_numeric_cols)}")
        
        # Create figure
        plt.figure(figsize=(12, 10))
        
        colorscale = self.config.get('heatmap_colorscale', 'RdYlGn')
        sns.heatmap(df, annot=annot, cmap=colorscale, center=0,
                   square=True, linewidths=1, cbar_kws={"shrink": 0.8})
        
        plt.title(title, fontsize=16, pad=20)
        plt.tight_layout()
        
        # Save figure
        if not output_path:
            output_path = f"heatmap_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        image_format = self.config.get('image_format', 'png')
        dpi = self.config.get('image_dpi', 300)
        
        plt.savefig(output_path, format=image_format, dpi=dpi, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_seaborn_bar_chart(self, df: pd.DataFrame, x_column: str, y_column: str,
                                title: str = "Bar Chart", output_path: str = None) -> str:
        """
        Create bar chart using Seaborn
        
        Args:
            df: DataFrame with data
            x_column: Column for x-axis
            y_column: Column for y-axis
            title: Chart title
            output_path: Path to save image file
            
        Returns:
            Path to saved image file
        """
        if df.empty:
            raise ValueError("Cannot create visualization: DataFrame is empty")
        
        if x_column not in df.columns or y_column not in df.columns:
            raise ValueError(f"Required columns not found in DataFrame")
        
        plt.figure(figsize=(12, 6))
        
        sns.barplot(data=df, x=x_column, y=y_column, palette="viridis")
        
        plt.title(title, fontsize=16, pad=20)
        plt.xlabel(x_column, fontsize=12)
        plt.ylabel(y_column, fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Save figure
        if not output_path:
            output_path = f"barchart_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        image_format = self.config.get('image_format', 'png')
        dpi = self.config.get('image_dpi', 300)
        
        plt.savefig(output_path, format=image_format, dpi=dpi, bbox_inches='tight')
        plt.close()
        
        return output_path
