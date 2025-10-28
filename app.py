import streamlit as st
import pandas as pd
import numpy as np
import json
import time
import base64

st.set_page_config(page_title="Policy Compliance Sandbox", layout="wide")

if "policies" not in st.session_state:
    st.session_state.policies = []
if "datasets" not in st.session_state:
    st.session_state.datasets = {}
if "violations" not in st.session_state:
    st.session_state.violations = pd.DataFrame()
if "trend_data" not in st.session_state:
    st.session_state.trend_data = pd.DataFrame(columns=["Date", "ComplianceScore"])

st.title("Policy Compliance Sandbox")

st.sidebar.header("Configuration")
mode = st.sidebar.selectbox("Select Role", ["Compliance Analyst", "System Administrator", "Auditor"])
st.sidebar.write(f"Current Role: {mode}")

st.header("1. Upload Policy and Data")
col1, col2 = st.columns(2)
with col1:
    policy_file = st.file_uploader("Upload Policy Document (PDF or DOCX)", type=["pdf", "docx"])
    if policy_file:
        st.session_state.policies.append(policy_file.name)
        st.success("Policy uploaded: " + policy_file.name)
with col2:
    dataset_file = st.file_uploader("Upload Compliance Dataset (CSV)", type=["csv"])
    if dataset_file:
        df = pd.read_csv(dataset_file)
        st.session_state.datasets[dataset_file.name] = df
        st.success("Dataset uploaded: " + dataset_file.name)

st.header("2. Run Compliance Analysis")
if st.button("Analyze Datasets"):
    if not st.session_state.datasets:
        st.error("No datasets uploaded")
    else:
        data_frames = []
        for name, data in st.session_state.datasets.items():
            if "Password_Age" in data.columns and "MFA_Enabled" in data.columns:
                data["Policy_Type"] = "Authentication"
                data["Violation"] = np.where((data["Password_Age"] > 90) | (data["MFA_Enabled"] == False), True, False)
                data["Severity_Score"] = np.where(data["Violation"], np.random.randint(60, 100, len(data)), 0)
                data_frames.append(data)
            elif "Patch_Level" in data.columns:
                data["Policy_Type"] = "System Security"
                data["Violation"] = np.where(data["Patch_Level"] < 3, True, False)
                data["Severity_Score"] = np.where(data["Violation"], np.random.randint(40, 90, len(data)), 0)
                data_frames.append(data)
        if data_frames:
            st.session_state.violations = pd.concat(data_frames)
            st.success("Compliance analysis complete")

if not st.session_state.violations.empty:
    df = st.session_state.violations
    st.header("3. Violation Dashboard")
    st.metric("Total Records", len(df))
    st.metric("Total Violations", df["Violation"].sum())
    st.metric("Average Severity", round(df["Severity_Score"].mean(), 2))
    heatmap = df.groupby("Policy_Type")["Violation"].sum().reset_index()
    st.bar_chart(heatmap, x="Policy_Type", y="Violation")
    st.subheader("Violation Details")
    st.dataframe(df)
    total_score = 100 - df["Violation"].mean() * 100
    new_entry = pd.DataFrame({"Date": [time.strftime("%Y-%m-%d")], "ComplianceScore": [total_score]})
    st.session_state.trend_data = pd.concat([st.session_state.trend_data, new_entry]).drop_duplicates("Date", keep="last")
    st.header("4. Compliance Trend")
    st.line_chart(st.session_state.trend_data, x="Date", y="ComplianceScore")

st.header("5. Export Reports")
if not st.session_state.violations.empty:
    csv = st.session_state.violations.to_csv(index=False).encode()
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="compliance_report.csv">Download CSV Report</a>'
    st.markdown(href, unsafe_allow_html=True)

st.header("6. Simulation Scenarios")
if not st.session_state.violations.empty:
    scenario = st.selectbox("Select Scenario", ["Enable MFA for all users", "Full Patch Deployment"])
    if st.button("Run Simulation"):
        df = st.session_state.violations.copy()
        if scenario == "Enable MFA for all users":
            df["MFA_Enabled"] = True
        elif scenario == "Full Patch Deployment" and "Patch_Level" in df.columns:
            df["Patch_Level"] = 5
        df["Violation"] = np.where((df.get("Password_Age", 0) > 90) | (df.get("MFA_Enabled", True) == False), True, False)
        df["Severity_Score"] = np.where(df["Violation"], np.random.randint(40, 80, len(df)), 0)
        st.subheader("Simulated Compliance Improvement")
        st.dataframe(df)
        improvement = 100 - df["Violation"].mean() * 100
        st.metric("Projected Compliance Score", round(improvement, 2))
