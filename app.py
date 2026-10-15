import os
import pandas as pd
import snowflake.connector
import streamlit as st

# Set page configuration first
st.set_page_config(
    page_title="AttritionIQ - HR Analytics", page_icon="⚡", layout="wide"
)

# Load environment variables if running locally
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


@st.cache_data(ttl=600)
def load_data():
    # Safely retrieve secrets with fallbacks
    def get_cred(key):
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
        return os.getenv(key)

    user = get_cred("SNOWFLAKE_USER")
    password = get_cred("SNOWFLAKE_PASSWORD")
    account = get_cred("SNOWFLAKE_ACCOUNT")
    warehouse = get_cred("SNOWFLAKE_WAREHOUSE")
    database = get_cred("SNOWFLAKE_DATABASE")
    schema = get_cred("SNOWFLAKE_SCHEMA")
    role = get_cred("SNOWFLAKE_ROLE")

    # Validate that credentials exist before connecting
    if not user or not password or not account:
        st.error(
            "⚠️ Missing Snowflake credentials! Please configure Streamlit Cloud Secrets."
        )
        st.stop()

    try:
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            role=role,
            warehouse=warehouse,
            database=database,
            schema=schema,
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM HR_ATTRITION_FINAL;")
        df = cursor.fetch_pandas_all()
        cursor.close()
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Snowflake Connection Error: {str(e)}")
        st.stop()


# App Title
st.title("⚡ AttritionIQ: HR Analytics & Retention Intelligence")

# Fetch Data
with st.spinner("Connecting to Snowflake and loading data..."):
    df = load_data()

st.success(f"Successfully loaded {len(df)} records from Snowflake!")
st.dataframe(df.head())