import pandas as pd
import streamlit as st
from src.connect_snowflake import get_snowflake_connection

st.set_page_config(
    page_title="AttritionIQ - HR Analytics", page_icon="⚡", layout="wide"
)

st.title("⚡ AttritionIQ: HR Analytics & Retention Intelligence")


@st.cache_data(ttl=600)
def load_data():
    conn = get_snowflake_connection()
    query = "SELECT * FROM HR_ATTRITION.RAW.HR_ATTRITION_FINAL;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


try:
    with st.spinner("Connecting to Snowflake and fetching HR dataset..."):
        df = load_data()

    st.success(f"Successfully loaded {len(df)} records!")
    st.dataframe(df.head())

except Exception as e:
    st.error("Failed to load data from Snowflake.")
    st.exception(e)  # Prints full traceback on the app interface