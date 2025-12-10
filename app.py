import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pdfplumber
import docx
import re

st.set_page_config(page_title="Policy Compliance Sandbox", page_icon="Shield", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    .main {background:#f9fbfc; color:#2d3748;}
    h1, h2, h3, h4 {font-family:'Inter',sans-serif; color:#1e293b; text-align:center;}
    .glow-title {font-size:3.5rem; font-weight:700; color:#2c5282;}
    .card {background:#ffffff; border-radius:16px; padding:32px; border:1px solid #e2e8f0; box-shadow:0 8px 25px rgba(0,0,0,0.05);}
    .upload-zone {border:2px dashed #cbd5e1; border-radius:20px; padding:60px 20px; text-align:center; background:#f8fafc; min-height:320px; display:flex; flex-direction:column; justify-content:center; align-items:center;}
    .upload-zone:hover {border-color:#63b3ed; background:#ebf8ff;}
    .upload-icon {font-size:4rem; margin-bottom:16px;}
    .stButton>button {background:#5dade2; color:white; font-weight:600; border:none; border-radius:12px; padding:16px 40px; font-size:18px;}
    .stButton>button:hover {background:#3c99dc;}
    .metric-box {background:#ffffff; border-radius:16px; padding:28px; text-align:center; border:1px solid #e2e8f0; box-shadow:0 4px 15px rgba(0,0,0,0.04);}
    .big-number {font-size:3rem; font-weight:700; color:#2d3748;}
    .footer {text-align:center; padding:40px; color:#718096; font-size:14px; margin-top:80px;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='glow-title'>POLICY COMPLIANCE SANDBOX</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;color:#718096;margin-top:-10px;'>Next-Gen Offline GRC Intelligence • TechGuard Solutions</h4>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1,2,1])
with c2:
    st.markdown("<h5 style='text-align:center;color:#4a5568;'>Role: " + st.selectbox("",["Compliance Analyst","HR Manager","IT Administrator","Auditor","System Admin"],key="role",label_visibility="collapsed") + "</h5>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

if "data" not in st.session_state: st.session_state.data = pd.DataFrame()
if "rules" not in st.session_state: st.session_state.rules = []
if "violations" not in st.session_state: st.session_state.violations = pd.DataFrame()

st.markdown("<h2>Upload Policy & Dataset</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="small")
with col1:
    st.markdown("<h3>Policy Document</h3><p>PDF • DOCX</p>", unsafe_allow_html=True)
    uploaded_policy = st.file_uploader("", type=["pdf","docx"], label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<h3>Compliance Dataset</h3><p>CSV • Excel</p>", unsafe_allow_html=True)
    uploaded_data = st.file_uploader("", type=["csv","xlsx"], label_visibility="collapsed", key="data_up")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Load Demo Data • Instant Preview", use_container_width=True, type="primary"):
    demo = pd.DataFrame({"user_id":["U001","U002","U003","U004","U005","U006","U007","U008","U009","U010"],
                         "department":["Finance","IT","HR","Finance","IT","Sales","HR","Finance","Legal","Ops"],
                         "mfa_enabled":[False,True,False,False,True,False,False,False,True,False],
                         "last_password_change":["2024-03-01","2025-11-01","2024-01-10","2023-10-20","2025-09-15","2024-02-28","2024-04-01","2023-08-15","2025-08-20","2024-05-05"],
                         "last_patch_date":["2024-07-01","2025-11-20","2024-06-10","2024-04-01","2025-11-05","2024-03-20","2024-05-30","2024-02-28","2025-10-10","2024-01-01"]})
    demo["last_password_change"] = pd.to_datetime(demo["last_password_change"])
    demo["last_patch_date"] = pd.to_datetime(demo["last_patch_date"])
    st.session_state.data = demo
    st.success("Demo data loaded")
    st.rerun()

def read_file(file):
    if not file: return None
    if file.name.endswith(('.xlsx','.xls')): return pd.read_excel(file)
    for enc in ['utf-8','utf-8-sig','latin-1','cp1252','iso-8859-1']:
        try: file.seek(0); return pd.read_csv(file, encoding=enc)
        except: continue
    st.error("Cannot read file encoding")
    return None

def extract_text(file):
    if file.name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as p:
            for page in p.pages:
                t = page.extract_text()
                if t: text += t + "\n"
        return text
    else:
        return "\n".join([p.text for p in docx.Document(file).paragraphs])

if uploaded_policy:
    with st.spinner("Analyzing policy document"):
        txt = extract_text(uploaded_policy)
        pats = [r"password.{0,30}every\s+(\d+)", r"MFA.{0,30}required", r"patch.{0,40}within\s+(\d+)"]
        found = []
        for p in pats:
            found.extend(re.findall(p, txt, re.IGNORECASE))
        st.session_state.rules = found or ["Password every 90 days", "MFA required", "Patches within 30 days"]
        st.success(f"Extracted {len(st.session_state.rules)} rules")

if uploaded_data:
    df = read_file(uploaded_data)
    if df is not None:
        cols = ["user_id","department","mfa_enabled","last_password_change","last_patch_date"]
        if all(c in df.columns for c in cols):
            df["last_password_change"] = pd.to_datetime(df["last_password_change"], errors='coerce')
            df["last_patch_date"] = pd.to_datetime(df["last_patch_date"], errors='coerce')
            st.session_state.data = df
            st.success(f"Loaded {len(df):,} records")
        else:
            st.error("Missing columns")

if not st.session_state.data.empty:
    st.markdown("<h2>Compliance Engine Settings</h2>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    pwd_thr = s1.slider("Password Age Limit (days)", 30, 180, 90, 5)
    patch_thr = s2.slider("Patch Age Limit (days)", 7, 90, 30, 1)
    mfa_on = s3.checkbox("MFA Mandatory", True)
    risk_weight = s4.select_slider("Risk Sensitivity", options=["Low","Medium","High","Extreme"], value="High")
    st.markdown("<br><br>", unsafe_allow_html=True)

if not st.session_state.data.empty:
    if st.button("LAUNCH COMPLIANCE SCAN", type="primary", use_container_width=True):
        with st.spinner("Scanning every user & device"):
            viol = []
            today = datetime.now()
            for _, r in st.session_state.data.iterrows():
                pwd = (today - r.last_password_change).days if pd.notna(r.last_password_change) else 999
                pat = (today - r.last_patch_date).days if pd.notna(r.last_patch_date) else 999
                mfa = str(r.mfa_enabled).lower() in ["true","1","yes"]
                if pwd > pwd_thr:
                    sev = 10 if pwd>180 else 8
                    viol.append({"user_id":r.user_id,"department":r.department,"violation":"Password Expired","severity":sev,"days":pwd})
                if not mfa and mfa_on:
                    viol.append({"user_id":r.user_id,"department":r.department,"violation":"MFA Missing","severity":10,"days":0})
                if pat > patch_thr:
                    viol.append({"user_id":r.user_id,"department":r.department,"violation":"Unpatched Device","severity":9,"days":pat})
            vdf = pd.DataFrame(viol)
            st.session_state.violations = vdf
            st.balloons()
            st.success(f"SCAN COMPLETE • {len(vdf)} VIOLATIONS DETECTED")

if not st.session_state.violations.empty:
    vdf = st.session_state.violations
    total = len(st.session_state.data)
    comp = round((1 - len(vdf)/total) * 100, 2)
    st.markdown("<h1 class='glow-title'>COMPLIANCE COMMAND CENTER</h1>", unsafe_allow_html=True)
    m1,m2,m3,m4 = st.columns(4)
    m1.markdown(f"<div class='metric-box'><h2 class='big-number'>{len(vdf)}</h2><p>Total Violations</p></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='metric-box'><h2 class='big-number' style='color:#e53e3e'>{len(vdf[vdf.severity>=9])}</h2><p>CRITICAL</p></div>", unsafe_allow_html=True)
    m3.markdown(f"<div class='metric-box'><h2 class='big-number' style='color:#dd6b20'>{len(vdf[vdf.severity==8])}</h2><p>HIGH RISK</p></div>", unsafe_allow_html=True)
    m4.markdown(f"<div class='metric-box'><h2 class='big-number' style='color:#38a169'>{comp}%</h2><p>COMPLIANCE SCORE</p></div>", unsafe_allow_html=True)
    t1, t2, t3, t4 = st.tabs(["Risk Galaxy", "Heat Matrix", "What-If Engine", "Raw Data"])
    with t1:
        fig = px.sunburst(vdf, path=['department','violation'], values='severity', color='severity', color_continuous_scale='Blues')
        fig.update_layout(margin=dict(t=30,l=0,r=0,b=0), height=700)
        st.plotly_chart(fig, use_container_width=True)
    with t2:
        fig = px.treemap(vdf, path=['department','violation'], values='severity', color='severity', color_continuous_scale='Purples', hover_data=['days'])
        fig.update_layout(margin=dict(t=30,l=0,r=0,b=0), height=700)
        st.plotly_chart(fig, use_container_width=True)
    with t3:
        st.markdown("### What-If Scenario Simulator")
        action = st.selectbox("Select Remediation", ["Enforce MFA Enterprise-Wide","Force Global Password Reset","Patch All Devices","Full Compliance Package"])
        if action == "Enforce MFA Enterprise-Wide": res = len(vdf[vdf.violation=="MFA Missing"])
        elif "Password" in action: res = len(vdf[vdf.violation=="Password Expired"])
        elif "Patch" in action: res = len(vdf[vdf.violation=="Unpatched Device"])
        else: res = len(vdf)
        new = round((total - (len(vdf)-res)) / total * 100, 2)
        colA, colB = st.columns(2)
        colA.metric("Current Compliance", f"{comp}%")
        colB.metric("After Action", f"{new}%", delta=f"{new-comp:+.2f}%")
        if st.button("EXECUTE SIMULATION"):
            st.success(f"{action} → {res} issues resolved")
            st.snow()
    with t4:
        st.dataframe(vdf.style.background_gradient(cmap='Blues', subset=['severity']), use_container_width=True)
    csv = vdf.to_csv(index=False).encode()
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.download_button("DOWNLOAD FULL REPORT (CSV)", csv, "Policy_Compliance_Report.csv", "text/csv", use_container_width=True)
else:
    st.markdown("""
    <div style='text-align:center; padding:120px 20px;'>
        <h1 class='glow-title'>Ready for Launch</h1>
        <p style='font-size:26px; color:#718096;'>Upload your policy & data<br>or click <b>Load Demo Data</b> to begin</p>
    </div>
    """, unsafe_allow_html=True)
