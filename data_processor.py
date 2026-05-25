"""
Data Processor Module
Handles CSV loading, data cleaning, validation, aggregation, and transformation
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Callable
from config import DATA_CONFIG


class DataProcessor:
    """Processes raw CSV datasets with cleaning, validation, and transformation"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize DataProcessor with configuration"""
        self.config = config or DATA_CONFIG
        
    def load_csv(self, filepath: str, encoding: str = 'utf-8') -> pd.DataFrame:
        """
        Load CSV dataset into a Pandas DataFrame
        
        Args:
            filepath: Path to the CSV file
            encoding: File encoding (default: utf-8)
            
        Returns:
            Pandas DataFrame containing the loaded data
            
        Raises:
            FileNotFoundError: If the CSV file doesn't exist
            ValueError: If the file cannot be parsed
        """
        try:
            df = pd.read_csv(filepath, encoding=encoding)
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {filepath}")
        except Exception as e:
            raise ValueError(f"Error loading CSV file: {str(e)}")
    
    def handle_missing_values(self, df: pd.DataFrame, strategy: str = None) -> pd.DataFrame:
        """
        Handle missing values according to configured strategy
        
        Args:
            df: Input DataFrame
            strategy: Strategy for handling missing values
                     ('drop', 'fill_mean', 'fill_median', 'fill_zero')
            
        Returns:
            DataFrame with missing values handled
        """
        strategy = strategy or self.config.get('missing_value_strategy', 'drop')
        df_copy = df.copy()
        
        if strategy == 'drop':
            df_copy = df_copy.dropna()
        elif strategy == 'fill_mean':
            numeric_cols = df_copy.select_dtypes(include=[np.number]).columns
            df_copy[numeric_cols] = df_copy[numeric_cols].fillna(df_copy[numeric_cols].mean())
        elif strategy == 'fill_median':
            numeric_cols = df_copy.select_dtypes(include=[np.number]).columns
            df_copy[numeric_cols] = df_copy[numeric_cols].fillna(df_copy[numeric_cols].median())
        elif strategy == 'fill_zero':
            df_copy = df_copy.fillna(0)
        else:
            raise ValueError(f"Unknown missing value strategy: {strategy}")
            
        return df_copy
    
    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate records from DataFrame
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with duplicates removed
        """
        return df.drop_duplicates()
    
    def convert_data_types(self, df: pd.DataFrame, type_mapping: Dict[str, str] = None) -> pd.DataFrame:
        """
        Convert columns to appropriate data types
        
        Args:
            df: Input DataFrame
            type_mapping: Dictionary mapping column names to data types
            
        Returns:
            DataFrame with converted data types
        """
        df_copy = df.copy()
        
        if type_mapping:
            for col, dtype in type_mapping.items():
                if col in df_copy.columns:
                    try:
                        if dtype == 'datetime':
                            df_copy[col] = pd.to_datetime(df_copy[col])
                        else:
                            df_copy[col] = df_copy[col].astype(dtype)
                    except Exception as e:
                        raise ValueError(f"Error converting column {col} to {dtype}: {str(e)}")
        
        return df_copy
    
    def validate_required_columns(self, df: pd.DataFrame, required_columns: List[str] = None) -> bool:
        """
        Validate that required columns exist in the DataFrame
        
        Args:
            df: Input DataFrame
            required_columns: List of required column names
            
        Returns:
            True if all required columns exist
            
        Raises:
            ValueError: If required columns are missing
        """
        required_columns = required_columns or self.config.get('required_columns', [])
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        
        return True
    
    def process_csv(self, filepath: str, required_columns: List[str] = None,
                   type_mapping: Dict[str, str] = None) -> pd.DataFrame:
        """
        Complete CSV processing pipeline
        
        Args:
            filepath: Path to CSV file
            required_columns: List of required columns
            type_mapping: Column data type mapping
            
        Returns:
            Processed DataFrame
        """
        # Load CSV
        df = self.load_csv(filepath)
        
        # Validate required columns
        self.validate_required_columns(df, required_columns)
        
        # Convert data types
        if type_mapping:
            df = self.convert_data_types(df, type_mapping)
        
        # Handle missing values
        df = self.handle_missing_values(df)
        
        # Remove duplicates
        if self.config.get('remove_duplicates', True):
            df = self.remove_duplicates(df)
        
        return df
    
    def aggregate_data(self, df: pd.DataFrame, group_by: List[str],
                      agg_functions: Dict[str, str]) -> pd.DataFrame:
        """
        Perform grouping and aggregation operations
        
        Args:
            df: Input DataFrame
            group_by: List of columns to group by
            agg_functions: Dictionary mapping columns to aggregation functions
                          (e.g., {'revenue': 'sum', 'profit': 'mean'})
            
        Returns:
            Aggregated DataFrame
            
        Raises:
            ValueError: If aggregation fails due to data type mismatches
        """
        try:
            result = df.groupby(group_by).agg(agg_functions).reset_index()
            return result
        except Exception as e:
            raise ValueError(f"Aggregation failed: {str(e)}")
    
    def pivot_data(self, df: pd.DataFrame, index: str, columns: str,
                  values: str, aggfunc: str = 'sum') -> pd.DataFrame:
        """
        Pivot data from long format to wide format
        
        Args:
            df: Input DataFrame
            index: Column to use as index
            columns: Column to use as columns
            values: Column to aggregate
            aggfunc: Aggregation function
            
        Returns:
            Pivoted DataFrame
        """
        try:
            result = df.pivot_table(index=index, columns=columns,
                                   values=values, aggfunc=aggfunc)
            return result.reset_index()
        except Exception as e:
            raise ValueError(f"Pivot operation failed: {str(e)}")
    
    def merge_datasets(self, df1: pd.DataFrame, df2: pd.DataFrame,
                      on: List[str], how: str = 'inner') -> pd.DataFrame:
        """
        Merge multiple datasets using common key columns
        
        Args:
            df1: First DataFrame
            df2: Second DataFrame
            on: List of key columns to merge on
            how: Type of merge ('inner', 'left', 'right', 'outer')
            
        Returns:
            Merged DataFrame
        """
        try:
            result = pd.merge(df1, df2, on=on, how=how)
            return result
        except Exception as e:
            raise ValueError(f"Merge operation failed: {str(e)}")
    
    def apply_transformation(self, df: pd.DataFrame, column: str,
                           transform_func: Callable) -> pd.DataFrame:
        """
        Apply custom transformation function to a column
        
        Args:
            df: Input DataFrame
            column: Column name to transform
            transform_func: Function to apply to the column
            
        Returns:
            DataFrame with transformed column
        """
        df_copy = df.copy()
        try:
            df_copy[column] = df_copy[column].apply(transform_func)
            return df_copy
        except Exception as e:
            raise ValueError(f"Transformation failed on column {column}: {str(e)}")
