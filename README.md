# Policy Compliance Sandbox

## Overview
**Policy Compliance Sandbox** is a prototype system designed to automate policy compliance verification and analysis within organizations. Developed by **TechGuard Solutions**, this project helps compliance analysts and administrators identify, score, and manage violations across HR, IT, and security policies through automated rule extraction and interactive dashboards.

The system provides a sandbox environment to simulate compliance checks using mock datasets and documents, making it ideal for training, experimentation, and research in governance and risk management.

---

## Key Features

### Policy & Data Upload
- Upload HR or IT policy documents (PDF, DOCX) for rule extraction.
- Upload structured datasets (CSV) such as password age, patch history, or MFA status.

### Automated Compliance Analysis
- Detect and categorize policy violations automatically.
- Assign and visualize severity scores based on rule criticality and risk.
- Generate actionable recommendations for remediation.

### Dashboards & Reports
- Interactive dashboards with:
  - Compliance heatmaps by department or system.
  - Trend charts to track improvement or decline.
  - Drillable tables for detailed violation insights.
- Exportable reports in **CSV** or **PDF** format for audits and management review.

### Scenario Simulations
- “What-if” analysis to simulate compliance improvements (e.g., enforcing MFA).
- Visualize projected compliance scores and trends after simulated changes.

### User & Role Management
- Role-based access for:
  - **System Administrators:** Manage users and roles.
  - **Compliance Analysts:** Analyze data, configure rules, and review violations.
  - **HR Managers / IT Admins:** Resolve assigned issues.
  - **Auditors:** Read-only access to historical data and reports.

---

## Technical Details

### Technology Stack
- **Language:** Python  
- **Framework:** Streamlit  
- **Data Format:** CSV for datasets, JSON for configuration  
- **Visualization:** Streamlit native components (heatmaps, tables, metrics)

### Architecture Highlights
- Modular design for progressive enhancement.
- Independent of paid APIs or cloud services — works with local datasets.
- Customizable rule engine supporting multiple policy types.
- Exportable and reproducible workflows for auditing.

---

## Non-Functional Goals
- **Performance:** Dashboards load within 3 seconds for datasets up to 10,000 records.  
- **Scalability:** Supports 50 concurrent users and datasets with 100,000 records.  
- **Security:** Role-based access, MFA enforcement, and GDPR compliance.  
- **Auditability:** Immutable logs and 5-year historical data retention.  
- **Accessibility:** WCAG 2.1 Level AA compliance.  
- **Reliability:** 99.5% uptime and automated daily backups.

---

## Future Enhancements
- Integration of advanced NLP models for automated policy rule extraction.
- AI-driven severity scoring and predictive compliance trends.
- Multi-language support and expanded visualization themes.
- Integration with real enterprise datasets or cloud connectors.

---

## Getting Started

**1. Clone the repository:
**   git clone https://github.com/your-username/policy-compliance-sandbox.git
   cd policy-compliance-sandbox

**2. Install dependencies:
**
  pip install -r requirements.txt

**3. Run the Streamlit app:
**
  streamlit run app.py


Access the system in your browser at http://localhost:8501
