import os
import snowflake.connector
import streamlit as st


def get_secret(key, default=""):
    # Check Streamlit Cloud secrets first, fallback to local environment variables
    if hasattr(st, "secrets") and key in st.secrets:
        return st.secrets[key]
    return os.getenv(key, default)


def get_snowflake_connection():
    conn = snowflake.connector.connect(
        user=get_secret("SNOWFLAKE_USER"),
        password=get_secret("SNOWFLAKE_PASSWORD"),
        account=get_secret("SNOWFLAKE_ACCOUNT"),
        role=get_secret("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
        warehouse=get_secret("SNOWFLAKE_WAREHOUSE", "HR_WH1"),
        database=get_secret("SNOWFLAKE_DATABASE", "HR_ATTRITION"),
        schema=get_secret("SNOWFLAKE_SCHEMA", "RAW"),
    )
    return conn