"""
Data Loader Module

Handles loading and filtering RCM event data from Databricks Delta tables.
Uses Databricks Secret Scope for secure credential management.
"""

from typing import Optional
import pandas as pd
from databricks.sdk import WorkspaceClient
from databricks import sql
from config import config
import os


class RCMDataLoader:
    """Loads RCM event data from Databricks Delta tables."""

    def __init__(self, catalog: str, schema: str, table: str):
        """
        Initialize the data loader.

        Args:
            catalog: Unity Catalog name
            schema: Schema name
            table: Table name
        """
        self.catalog = catalog
        self.schema = schema
        self.table = table
        self.full_table_name = f"{catalog}.{schema}.{table}"
        self.w = WorkspaceClient(token=config.DATABRICKS_TOKEN,auth_type="pat")
        self._connection = None

    def _get_connection(self):
        """Get Databricks SQL connection using environment variables."""
        if self._connection is None:
            # Get credentials from environment variables
            server_hostname = os.environ.get("DATABRICKS_HOST", "").replace("https://", "")
            http_path = os.environ.get("DATABRICKS_HTTP_PATH")
            access_token = os.environ.get("DATABRICKS_TOKEN")

            if not all([server_hostname, http_path, access_token]):
                raise ValueError(
                    "Missing required environment variables. Please set:\n"
                    "  - DATABRICKS_HOST (e.g., https://your-workspace.cloud.databricks.com)\n"
                    "  - DATABRICKS_HTTP_PATH (e.g., /sql/1.0/warehouses/abc123)\n"
                    "  - DATABRICKS_TOKEN (your personal access token)"
                )

            try:
                print(f"Connecting to Databricks at {server_hostname}...")
                self._connection = sql.connect(
                    server_hostname=server_hostname,
                    http_path=http_path,
                    access_token=access_token,
                )
                print("✓ Connected successfully!")
            except Exception as e:
                raise RuntimeError(f"Failed to connect to Databricks: {e}")

        return self._connection

    def _execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute a SQL query and return results as DataFrame.

        Args:
            query: SQL query string

        Returns:
            DataFrame with query results
        """
        # For local development, use SQL connector instead of Spark
        connection = self._get_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            return pd.DataFrame(result, columns=columns)
        else:
            raise RuntimeError(
                "Cannot execute query: SQL connection not available. "
                "Please check your DATABRICKS_HOST, DATABRICKS_HTTP_PATH, and DATABRICKS_TOKEN environment variables."
            )

    def load_data(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        department: Optional[str] = None,
        outcome: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> pd.DataFrame:
        """
        Load RCM event data with optional filters.

        Args:
            start_date: Filter events after this date (YYYY-MM-DD)
            end_date: Filter events before this date (YYYY-MM-DD)
            department: Filter by department
            outcome: Filter by outcome
            limit: Limit number of rows returned

        Returns:
            DataFrame with filtered RCM events
        """
        # Build query with filters
        where_clauses = []

        if start_date:
            where_clauses.append(f"timestamp >= '{start_date}'")

        if end_date:
            where_clauses.append(f"timestamp <= '{end_date}'")

        if department:
            where_clauses.append(f"department = '{department}'")

        if outcome:
            where_clauses.append(f"outcome = '{outcome}'")

        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"

        query = f"""
        SELECT
            entity_id,
            patient_id,
            doctor_id,
            hospital_id,
            insurance_id,
            activity_id,
            activity,
            activity_code,
            timestamp,
            activity_order,
            duration_minutes,
            cost_dollars,
            outcome,
            department
        FROM {self.full_table_name}
        WHERE {where_clause}
        ORDER BY entity_id, activity_order
        """

        if limit:
            query += f" LIMIT {limit}"

        print(f"Loading data from {self.full_table_name}...")
        df = self._execute_query(query)
        print(f"Loaded {len(df):,} events")

        return df

    def get_unique_values(self, column: str) -> list:
        """
        Get unique values for a specific column.

        Args:
            column: Column name

        Returns:
            List of unique values
        """
        query = f"""
        SELECT DISTINCT {column}
        FROM {self.full_table_name}
        ORDER BY {column}
        """

        df = self._execute_query(query)
        return df[column].tolist()

    def get_table_stats(self) -> dict:
        """
        Get basic statistics about the table.

        Returns:
            Dictionary with table statistics
        """
        query = f"""
        SELECT
            COUNT(*) as total_events,
            COUNT(DISTINCT entity_id) as total_journeys,
            COUNT(DISTINCT patient_id) as total_patients,
            COUNT(DISTINCT activity_code) as total_activities,
            MIN(timestamp) as min_date,
            MAX(timestamp) as max_date
        FROM {self.full_table_name}
        """

        df = self._execute_query(query)
        return df.iloc[0].to_dict()

    def close(self):
        """Close database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
