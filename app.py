import os
import sys

# 1. Fix module search path for Streamlit Cloud deployment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import pandas as pd
import streamlit as st

# 2. Flexible import handling for connect_snowflake module
try:
    from src.connect_snowflake import get_snowflake_connection
except ImportError:
    try:
        from connect_snowflake import get_snowflake_connection
    except ImportError:
        st.error(
            "Could not import 'get_snowflake_connection'. Ensure 'src/connect_snowflake.py' exists."
        )
        st.stop()

# Load environment variables for local testing
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# 3. Configure Streamlit Page
st.set_page_config(
    page_title="AttritionIQ - HR Analytics & Retention Intelligence",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ AttritionIQ: HR Analytics & Retention Intelligence")
st.markdown(
    "Transforming workforce data into predictive retention strategies and proactive HR interventions."
)


# 4. Data Loading Function with Caching
@st.cache_data(ttl=600)
def load_data():
    conn = get_snowflake_connection()
    # Fetch final merged table from Snowflake
    query = "SELECT * FROM HR_ATTRITION.RAW.HR_ATTRITION_FINAL;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# 5. Main Execution Flow & Dashboard Rendering
try:
    with st.spinner("Connecting to Snowflake and fetching HR dataset..."):
        df = load_data()

    st.success(f"Successfully connected to Snowflake! ({len(df)} records loaded)")

    # Key Workforce Metrics
    st.subheader("📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    total_emp = len(df)
    attrition_col = [col for col in df.columns if col.lower() == "attrition"]

    if attrition_col:
        attrition_count = df[df[attrition_col[0]].astype(str).str.upper() == "YES"].shape[0]
        attrition_rate = (attrition_count / total_emp) * 100 if total_emp > 0 else 0
    else:
        attrition_count = "N/A"
        attrition_rate = 0

    col1.metric("Total Employees", total_emp)
    col2.metric("Total Attrition", attrition_count)
    col3.metric(
        "Attrition Rate",
        f"{attrition_rate:.1f}%" if isinstance(attrition_rate, float) else "N/A",
    )

    if "MONTHLY_INCOME" in [c.upper() for c in df.columns]:
        income_col = [c for c in df.columns if c.upper() == "MONTHLY_INCOME"][0]
        avg_income = df[income_col].dropna().astype(float).mean()
        col4.metric("Avg Monthly Income", f"${avg_income:,.0f}")

    st.markdown("---")

    # HR Data Preview Table
    st.subheader("📋 Workforce Dataset Preview")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("⚠️ An error occurred while executing the application:")
    st.exception(e)