"""
SQL Extractor Module
Handles MySQL database connections and data extraction with optimized queries
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
from typing import Dict, List, Optional
from config import SQL_CONFIG, DB_CONFIG
import time


class SQLExtractor:
    """Extracts data from MySQL database with optimized queries"""
    
    def __init__(self, db_config: Dict = None, sql_config: Dict = None):
        """
        Initialize SQL Extractor
        
        Args:
            db_config: Database connection configuration
            sql_config: SQL execution configuration
        """
        self.db_config = db_config or DB_CONFIG
        self.sql_config = sql_config or SQL_CONFIG
        self.connection = None
    
    def connect(self) -> bool:
        """
        Establish connection to MySQL database
        
        Returns:
            True if connection successful
            
        Raises:
            ValueError: If connection fails with descriptive error
        """
        try:
            connection_timeout = self.sql_config.get('connection_timeout', 30)
            
            self.connection = mysql.connector.connect(
                host=self.db_config['host'],
                port=self.db_config['port'],
                user=self.db_config['username'],
                password=self.db_config['password'],
                database=self.db_config['database'],
                connection_timeout=connection_timeout
            )
            
            if self.connection.is_connected():
                return True
            else:
                raise ValueError("Connection established but not active")
                
        except Error as e:
            error_msg = (f"Database connection failed. "
                        f"Host: {self.db_config['host']}, "
                        f"Port: {self.db_config['port']}, "
                        f"Database: {self.db_config['database']}, "
                        f"Error: {str(e)}")
            raise ValueError(error_msg)
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query: str, timeout: int = None) -> pd.DataFrame:
        """
        Execute SELECT query and return results as DataFrame
        
        Args:
            query: SQL SELECT query string
            timeout: Query timeout in seconds
            
        Returns:
            Pandas DataFrame with query results
            
        Raises:
            ValueError: If query execution fails
        """
        if not self.connection or not self.connection.is_connected():
            self.connect()
        
        timeout = timeout or self.sql_config.get('max_query_timeout', 300)
        
        try:
            df = pd.read_sql(query, self.connection)
            return df
            
        except Error as e:
            error_msg = (f"Query execution failed. "
                        f"Error type: {type(e).__name__}, "
                        f"Query: {query[:100]}..., "
                        f"Error: {str(e)}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Query execution failed: {str(e)}"
            raise ValueError(error_msg)
    
    def execute_join_query(self, tables: List[str], join_conditions: List[Dict],
                          select_columns: List[str] = None,
                          where_clause: str = None) -> pd.DataFrame:
        """
        Execute multi-table join query
        
        Args:
            tables: List of table names
            join_conditions: List of join specifications
                           [{'type': 'INNER', 'table': 'table2', 'on': 'table1.id = table2.id'}]
            select_columns: List of columns to select (default: *)
            where_clause: Optional WHERE clause
            
        Returns:
            DataFrame with join results
        """
        # Build SELECT clause
        if select_columns:
            select_clause = ', '.join(select_columns)
        else:
            select_clause = '*'
        
        # Build FROM clause
        query = f"SELECT {select_clause} FROM {tables[0]}"
        
        # Build JOIN clauses
        for join in join_conditions:
            join_type = join.get('type', 'INNER')
            join_table = join['table']
            join_on = join['on']
            query += f" {join_type} JOIN {join_table} ON {join_on}"
        
        # Add WHERE clause
        if where_clause:
            query += f" WHERE {where_clause}"
        
        return self.execute_query(query)
    
    def calculate_rolling_average(self, table: str, value_column: str,
                                  date_column: str, window_days: int,
                                  group_by: List[str] = None,
                                  where_clause: str = None) -> pd.DataFrame:
        """
        Calculate rolling average using SQL window functions
        
        Args:
            table: Table name
            value_column: Column to calculate rolling average on
            date_column: Date column for ordering
            window_days: Number of days for rolling window
            group_by: Optional columns to partition by
            where_clause: Optional WHERE clause
            
        Returns:
            DataFrame with rolling average
        """
        # Validate window size
        if window_days < 1 or window_days > 365:
            raise ValueError(f"Window size must be between 1 and 365 days, got {window_days}")
        
        # Build partition clause
        partition_clause = ""
        if group_by:
            partition_clause = f"PARTITION BY {', '.join(group_by)}"
        
        # Build query with window function
        query = f"""
        SELECT 
            *,
            AVG({value_column}) OVER (
                {partition_clause}
                ORDER BY {date_column}
                ROWS BETWEEN {window_days - 1} PRECEDING AND CURRENT ROW
            ) as rolling_avg_{window_days}d
        FROM {table}
        """
        
        if where_clause:
            query += f" WHERE {where_clause}"
        
        query += f" ORDER BY {date_column}"
        
        return self.execute_query(query)
    
    def execute_aggregation_query(self, table: str, group_by: List[str],
                                 aggregations: Dict[str, str],
                                 where_clause: str = None,
                                 having_clause: str = None) -> pd.DataFrame:
        """
        Execute aggregation query with GROUP BY
        
        Args:
            table: Table name
            group_by: Columns to group by
            aggregations: Dict mapping column to aggregation function
                         {'revenue': 'SUM', 'orders': 'COUNT'}
            where_clause: Optional WHERE clause
            having_clause: Optional HAVING clause
            
        Returns:
            DataFrame with aggregated results
        """
        # Build SELECT clause
        select_parts = group_by.copy()
        for col, func in aggregations.items():
            select_parts.append(f"{func}({col}) as {col}_{func.lower()}")
        
        select_clause = ', '.join(select_parts)
        group_clause = ', '.join(group_by)
        
        query = f"SELECT {select_clause} FROM {table}"
        
        if where_clause:
            query += f" WHERE {where_clause}"
        
        query += f" GROUP BY {group_clause}"
        
        if having_clause:
            query += f" HAVING {having_clause}"
        
        return self.execute_query(query)
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
