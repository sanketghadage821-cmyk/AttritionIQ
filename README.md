# ⚡ AttritionIQ: HR Analytics & Retention Intelligence

A machine learning-powered web application built with **Streamlit**, **Snowflake**, and **Scikit-Learn** that provides actionable insights into employee attrition drivers and real-time risk predictions for proactive HR interventions.

🚀 **Live App**: [attritioniq-c7yyzx9zpgy2bqsybwsnwh.streamlit.app](https://attritioniq-c7yyzx9zpgy2bqsybwsnwh.streamlit.app/)

---

## 📌 Project Overview

**AttritionIQ** allows HR teams and business leaders to:
- **Analyze Workforce Trends**: View overall attrition rates, satisfaction scores, income distributions, and department-level turnover.
- **Cross-Filter Visualizations**: Dynamically drill down into data across departments, tenure ranges, overtime, and performance ratings.
- **Predict Attrition Risk**: Predict individual employee churn probability using a trained Machine Learning model.
- **Identify Drivers**: Understand top factors causing turnover using model-based feature importances.

---

## 🏗️ Architecture & Stack

- **Frontend / UI**: [Streamlit](https://streamlit.io/) (Interactive Dashboard)
- **Data Warehouse**: [Snowflake](https://www.snowflake.com/) (Raw & Cleaned HR Datasets)
- **Data Engineering**: SQL Transformation Pipelines (`HR_ATTRITION.RAW.HR_ATTRITION_FINAL`)
- **Machine Learning**: Scikit-Learn (Random Forest / Decision Tree Classifier with categorical encoders)
- **Visualization**: Plotly Express

---

## 📁 Repository Structure

```text
AttritionIQ/
├── .env                       # Local environment variables (git-ignored)
├── .gitignore                 # Files excluded from version control
├── README.md                  # Project documentation
├── app.py                     # Main Streamlit dashboard application
├── main.py                    # Project orchestration / runner
├── requirements.txt           # Python dependencies
├── models/
│   └── attrition_model.pkl    # Trained ML model and encoders
├── outputs/                   # Exported analytical plots
│   ├── attrition_by_department.png
│   ├── attrition_by_overtime.png
│   └── salary_vs_attrition.png
└── src/
    ├── __init__.py            # Python package initializer
    ├── connect_snowflake.py   # Database connection module
    ├── eda.py                 # Exploratory Data Analysis routines
    └── train_model.py         # Model training pipeline
