import os
import pandas as pd
import snowflake.connector
import streamlit as st

# Set page layout configuration
st.set_page_config(
    page_title="AttritionIQ - HR Analytics & Retention Intelligence",
    page_icon="⚡",
    layout="wide",
)

# Load environment variables if running locally
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


@st.cache_data(ttl=600)
def load_data():
    # Helper to check Streamlit Secrets first, then environment variables
    def get_cred(key):
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
        return os.getenv(key)

    user = get_cred("SNOWFLAKE_USER")
    password = get_cred("SNOWFLAKE_PASSWORD")
    account = get_cred("SNOWFLAKE_ACCOUNT")
    role = get_cred("SNOWFLAKE_ROLE") or "ACCOUNTADMIN"
    warehouse = get_cred("SNOWFLAKE_WAREHOUSE") or "COMPUTE_WH"
    database = get_cred("SNOWFLAKE_DATABASE") or "HR_DB"
    schema = get_cred("SNOWFLAKE_SCHEMA") or "PUBLIC"

    # Validate essential credentials
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

        # Try fully qualified uppercase table first, fallback to lowercase if needed
        try:
            cursor.execute(f"SELECT * FROM {database}.{schema}.HR_ATTRITION_FINAL;")
        except Exception:
            cursor.execute(f"SELECT * FROM {database}.{schema}.hr_attrition_final;")

        df = cursor.fetch_pandas_all()
        cursor.close()
        conn.close()

        # Standardize DataFrame column names to UPPERCASE
        df.columns = [col.upper() for col in df.columns]
        return df

    except Exception as e:
        st.error(f"❌ Snowflake Connection Error: {str(e)}")
        st.stop()


# --- APP INTERFACE ---

st.title("⚡ AttritionIQ: HR Analytics & Retention Intelligence")
st.markdown(
    "Transforming workforce data into predictive retention strategies and proactive HR interventions."
)

with st.spinner("Connecting to Snowflake and fetching HR dataset..."):
    df = load_data()

# Summary KPI Header Row
st.subheader("📊 Executive Overview Metrics")
col1, col2, col3, col4 = st.columns(4)

total_emp = len(df)
left_emp = len(df[df["ATTRITION"].astype(str).str.upper() == "YES"]) if "ATTRITION" in df.columns else 0
attrition_rate = (left_emp / total_emp * 100) if total_emp > 0 else 0.0

# Count High Risk Employees (Overtime + Low Salary/Tenure if present)
high_risk_count = 0
if "OVERTIME" in df.columns and "MONTHLY_INCOME" in df.columns:
    high_risk_count = len(
        df[(df["OVERTIME"].astype(str).str.upper() == "YES") & (df["MONTHLY_INCOME"] < 45000)]
    )

col1.metric("Total Headcount", f"{total_emp:,}")
col2.metric("Employees Departed", f"{left_emp:,}")
col3.metric("Attrition Rate", f"{attrition_rate:.1f}%")
col4.metric("Active High-Risk Pool", f"{high_risk_count:,}")

st.markdown("---")

# Data Preview & Search Section
st.subheader("📋 HR Dataset Records")
st.dataframe(df, use_container_width=True)