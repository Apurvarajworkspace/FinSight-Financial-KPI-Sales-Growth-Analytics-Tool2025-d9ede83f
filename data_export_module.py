"""
Data Export Module
Export data in multiple formats: CSV, Excel, JSON, PDF
"""

import json
import pandas as pd
import os
from datetime import datetime


class DataExporter:
    """Export data in multiple formats"""
    
    def __init__(self, output_dir='exports'):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def export_to_csv(self, data, filename, index=True):
        """
        Export data to CSV
        
        Args:
            data: DataFrame or dictionary
            filename: Output filename
            index: Include index
        
        Returns:
            Path to exported file
        """
        filepath = os.path.join(self.output_dir, filename)
        
        if isinstance(data, pd.DataFrame):
            data.to_csv(filepath, index=index)
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=index)
        else:
            raise ValueError("Data must be DataFrame or dict")
        
        return filepath
    
    def export_to_excel(self, data_dict, filename, include_summary=True):
        """
        Export multiple dataframes to Excel with multiple sheets
        
        Args:
            data_dict: Dictionary of {sheet_name: dataframe}
            filename: Output filename
            include_summary: Add summary sheet
        
        Returns:
            Path to exported file
        """
        filepath = os.path.join(self.output_dir, filename)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            for sheet_name, data in data_dict.items():
                if isinstance(data, pd.DataFrame):
                    data.to_excel(writer, sheet_name=sheet_name, index=True)
                elif isinstance(data, dict):
                    df = pd.DataFrame(data, index=[0])
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Add summary sheet
            if include_summary:
                summary_data = {
                    'Generated_At': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'Number_of_Sheets': len(data_dict),
                    'Sheets': ', '.join(data_dict.keys())
                }
                summary_df = pd.DataFrame(summary_data, index=[0]).T
                summary_df.columns = ['Value']
                summary_df.to_excel(writer, sheet_name='Summary')
        
        return filepath
    
    def export_to_json(self, data, filename, indent=2, orient='records'):
        """
        Export data to JSON
        
        Args:
            data: DataFrame or dictionary
            filename: Output filename
            indent: JSON indentation
            orient: DataFrame orient ('records', 'index', etc.)
        
        Returns:
            Path to exported file
        """
        filepath = os.path.join(self.output_dir, filename)
        
        if isinstance(data, pd.DataFrame):
            json_data = data.to_json(orient=orient, default_handler=str)
            with open(filepath, 'w') as f:
                f.write(json_data)
        elif isinstance(data, dict):
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=indent, default=str)
        else:
            raise ValueError("Data must be DataFrame or dict")
        
        return filepath
    
    def export_to_html(self, data_dict, filename, title='Data Export Report'):
        """
        Export data to HTML
        
        Args:
            data_dict: Dictionary of {section_name: dataframe}
            filename: Output filename
            title: Report title
        
        Returns:
            Path to exported file
        """
        filepath = os.path.join(self.output_dir, filename)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                h1 {{ color: #333; text-align: center; }}
                h2 {{ color: #666; margin-top: 30px; border-bottom: 2px solid #0066cc; }}
                table {{ 
                    border-collapse: collapse; 
                    width: 100%; 
                    margin: 20px 0; 
                    background-color: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                th {{ 
                    background-color: #0066cc; 
                    color: white; 
                    padding: 12px; 
                    text-align: left;
                    font-weight: bold;
                }}
                td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                tr:hover {{ background-color: #f9f9f9; }}
                .footer {{ 
                    text-align: center; 
                    color: #999; 
                    font-size: 12px; 
                    margin-top: 50px; 
                    border-top: 1px solid #ddd;
                    padding-top: 20px;
                }}
                .metric {{ font-weight: bold; color: #0066cc; }}
                .positive {{ color: green; }}
                .negative {{ color: red; }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            <p style="text-align: center; color: #999;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        """
        
        for section_name, data in data_dict.items():
            html_content += f"<h2>{section_name}</h2>"
            
            if isinstance(data, pd.DataFrame):
                html_content += data.to_html()
            elif isinstance(data, dict):
                df = pd.DataFrame(data, index=[0])
                html_content += df.to_html()
            elif isinstance(data, str):
                html_content += f"<p>{data}</p>"
        
        html_content += """
            <div class="footer">
                <p>Data Export Report | FinSight Analytics Platform</p>
            </div>
        </body>
        </html>
        """
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        return filepath
    
    def export_summary_report(self, metrics, filename='summary_report.json'):
        """
        Export executive summary
        
        Args:
            metrics: Metrics dictionary
            filename: Output filename
        
        Returns:
            Path to exported file
        """
        summary = {
            'generated_at': datetime.now().isoformat(),
            'report_title': 'Financial Analytics Summary',
            'metrics': {k: float(v) if isinstance(v, (int, float)) else str(v) 
                       for k, v in metrics.items()},
            'export_formats': ['JSON', 'CSV', 'Excel', 'HTML']
        }
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        return filepath


class ReportFormatter:
    """Format data for reporting"""
    
    @staticmethod
    def format_currency(value, currency='$', decimals=2):
        """Format as currency"""
        return f"{currency}{value:,.{decimals}f}"
    
    @staticmethod
    def format_percentage(value, decimals=2):
        """Format as percentage"""
        return f"{value:.{decimals}f}%"
    
    @staticmethod
    def format_number(value, decimals=2):
        """Format as number with thousands separator"""
        return f"{value:,.{decimals}f}"
    
    @staticmethod
    def create_formatted_table(df, currency_cols=None, percentage_cols=None):
        """
        Create formatted table for display
        
        Args:
            df: DataFrame to format
            currency_cols: Columns to format as currency
            percentage_cols: Columns to format as percentage
        
        Returns:
            Formatted DataFrame
        """
        formatted_df = df.copy()
        
        if currency_cols:
            for col in currency_cols:
                if col in formatted_df.columns:
                    formatted_df[col] = formatted_df[col].apply(
                        lambda x: ReportFormatter.format_currency(x) if isinstance(x, (int, float)) else x
                    )
        
        if percentage_cols:
            for col in percentage_cols:
                if col in formatted_df.columns:
                    formatted_df[col] = formatted_df[col].apply(
                        lambda x: ReportFormatter.format_percentage(x) if isinstance(x, (int, float)) else x
                    )
        
        return formatted_df


class BatchExporter:
    """Export multiple datasets efficiently"""
    
    def __init__(self, output_dir='exports'):
        self.exporter = DataExporter(output_dir)
        self.export_log = []
    
    def export_batch(self, exports_config):
        """
        Execute batch exports
        
        Args:
            exports_config: List of export configurations
                [{
                    'data': dataframe/dict,
                    'format': 'csv'/'excel'/'json'/'html',
                    'filename': 'filename',
                    'options': {optional parameters}
                }]
        
        Returns:
            List of exported files
        """
        exported_files = []
        
        for config in exports_config:
            try:
                data = config.get('data')
                format_type = config.get('format', 'csv').lower()
                filename = config.get('filename')
                options = config.get('options', {})
                
                if format_type == 'csv':
                    filepath = self.exporter.export_to_csv(data, filename, **options)
                elif format_type == 'excel':
                    filepath = self.exporter.export_to_excel(data, filename, **options)
                elif format_type == 'json':
                    filepath = self.exporter.export_to_json(data, filename, **options)
                elif format_type == 'html':
                    filepath = self.exporter.export_to_html(data, filename, **options)
                else:
                    raise ValueError(f"Unsupported format: {format_type}")
                
                exported_files.append(filepath)
                self.export_log.append({
                    'filename': filename,
                    'format': format_type,
                    'status': 'SUCCESS',
                    'timestamp': datetime.now().isoformat()
                })
            
            except Exception as e:
                self.export_log.append({
                    'filename': config.get('filename'),
                    'format': config.get('format'),
                    'status': 'FAILED',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        return exported_files
    
    def get_export_log(self):
        """Get export execution log"""
        return pd.DataFrame(self.export_log)
