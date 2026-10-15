<div align="center">

# ⚡ AttritionIQ: Enterprise HR Analytics & Retention Intelligence

[![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](#)
[![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?style=for-the-badge&logo=snowflake&logoColor=white)](#)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](#)
[![DAX](https://img.shields.io/badge/DAX-00758F?style=for-the-badge&logo=mdn&logoColor=white)](#)

<p align="center">
  <b>Transforming workforce data into predictive retention strategies.</b>
</p>

</div>

---

## 📌 Project Overview

> **AttritionIQ** is an end-to-end Enterprise HR Analytics platform designed to identify turnover drivers, model attrition risk, and provide HR teams with actionable retention lists before high-value employees exit.

---

## 📊 Executive Snapshot

| Total Headcount | Employees Departed | Overall Attrition Rate | Active High-Risk Employees |
| :---: | :---: | :---: | :---: |
| **4,700** | **1,359** | **28.9%** | **1,118** |

---

## 🎯 Key Attrition Drivers Identified

* ⚡ **Overtime Workload:** Attrition jumps to **41.6%** for overtime staff vs. **23.3%** for non-overtime roles.
* 💰 **Compensation Bands:** Staff earning under **₹45K/month** show the highest exit rate at **42.9%**.
* ⏳ **Tenure Vulnerability:** **40.2%** of exits occur within the first year (**0–1 years**), indicating onboarding gaps.
* 🚗 **Commute Strain:** Employees traveling **21+ km** daily exhibit an elevated exit rate (**36.3%**).

---

## ⚙️ Risk Scoring Algorithm

AttritionIQ dynamic risk scores evaluate 5 core operational indicators:

$$\text{Risk Score} = \text{Overtime} + \text{Low Pay (<45K)} + \text{Far Commute (>20km)} + \text{Low Tenure (<2yrs)} + \text{Low Satisfaction (\le 2)}$$

```dax
Risk Factors = 
  IF(HR_ATTRITION_FINAL[OVERTIME] = "Yes", 1, 0)
+ IF(HR_ATTRITION_FINAL[MONTHLY_INCOME] < 45000, 1, 0)
+ IF(HR_ATTRITION_FINAL[DISTANCE_FROM_HOME] > 20, 1, 0)
+ IF(HR_ATTRITION_FINAL[YEARS_AT_COMPANY] < 2, 1, 0)
+ IF(HR_ATTRITION_FINAL[JOB_SATISFACTION] <= 2, 1, 0)
