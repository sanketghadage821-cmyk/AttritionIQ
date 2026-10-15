import os
import snowflake.connector
import streamlit as st


@st.cache_data
def load_data():
    def get_cred(key):
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
        return os.getenv(key)

    conn = snowflake.connector.connect(
        user=get_cred("SNOWFLAKE_USER"),
        password=get_cred("SNOWFLAKE_PASSWORD"),
        account=get_cred("SNOWFLAKE_ACCOUNT"),
        role=get_cred("SNOWFLAKE_ROLE"),
        warehouse=get_cred("SNOWFLAKE_WAREHOUSE"),
        database=get_cred("SNOWFLAKE_DATABASE"),
        schema=get_cred("SNOWFLAKE_SCHEMA"),
    )

    cursor = conn.cursor()
    # Query table using uppercase name
    cursor.execute("SELECT * FROM HR_ATTRITION_FINAL;")
    df = cursor.fetch_pandas_all()

    cursor.close()
    conn.close()

    return df