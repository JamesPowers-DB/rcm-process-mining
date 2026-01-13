"""
Configuration Module

Centralized configuration for the RCM Process Mining Demo.
"""

import os
from typing import Optional


class Config:
    """Application configuration."""

    # Databricks connection
    DATABRICKS_HOST: str = os.environ.get("DATABRICKS_HOST", "")
    DATABRICKS_HTTP_PATH: str = os.environ.get("DATABRICKS_HTTP_PATH", "")
    DATABRICKS_TOKEN: str = os.environ.get("DATABRICKS_TOKEN", "")

    # Data source
    CATALOG_NAME: str = os.environ.get("CATALOG_NAME", "rcm_demo")
    SCHEMA_NAME: str = os.environ.get("SCHEMA_NAME", "process_mining")
    TABLE_NAME: str = os.environ.get("TABLE_NAME", "rcm_events")

    # App settings
    APP_PORT: int = int(os.environ.get("APP_PORT", "8080"))
    APP_DEBUG: bool = os.environ.get("APP_DEBUG", "False").lower() == "true"
    APP_HOST: str = os.environ.get("APP_HOST", "0.0.0.0")

    # Default filter values
    DEFAULT_GRANULARITY: int = 2
    DEFAULT_START_DATE: str = "2023-01-01"
    DEFAULT_END_DATE: str = "2024-12-31"

    # Performance settings
    MAX_ROWS_LOAD: Optional[int] = None  # None = no limit
    CACHE_TIMEOUT: int = 300  # seconds

    @classmethod
    def validate(cls) -> bool:
        """
        Validate configuration.

        Returns:
            True if configuration is valid

        Raises:
            ValueError if required configuration is missing
        """
        missing = []
        
        if not cls.DATABRICKS_HOST:
            missing.append("DATABRICKS_HOST (e.g., https://your-workspace.cloud.databricks.com)")
        
        if not cls.DATABRICKS_HTTP_PATH:
            missing.append("DATABRICKS_HTTP_PATH (e.g., /sql/1.0/warehouses/abc123)")
        
        if not cls.DATABRICKS_TOKEN:
            missing.append("DATABRICKS_TOKEN (your personal access token)")
        
        if missing:
            raise ValueError(
                "Missing required environment variables:\n  - " + 
                "\n  - ".join(missing) +
                "\n\nTo set them, run:\n" +
                "  export DATABRICKS_HOST='https://your-workspace.cloud.databricks.com'\n" +
                "  export DATABRICKS_HTTP_PATH='/sql/1.0/warehouses/your-warehouse-id'\n" +
                "  export DATABRICKS_TOKEN='your-token'"
            )

        return True

    @classmethod
    def get_full_table_name(cls) -> str:
        """Get fully qualified table name."""
        return f"{cls.CATALOG_NAME}.{cls.SCHEMA_NAME}.{cls.TABLE_NAME}"


# Create singleton instance
config = Config()
