# ID-Fintech-AI-Fairness: Agentic FinOps Audit (AFA)

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Compliance](https://img.shields.io/badge/Compliance-OJK_1%2F2026-success.svg)
![Data Privacy](https://img.shields.io/badge/Data_Privacy-UU_PDP_27%2F2022-success.svg)
![Status](https://img.shields.io/badge/Status-Production_Ready-green.svg)

A strategic, agentic diagnostic framework for auditing digital credit scoring and lending models in the Indonesian fintech ecosystem.

---

## Executive Summary: Mitigating Algorithmic Bias
### *A Strategic Framework for OJK-Compliant AI in Indonesian Fintech*

**Overview**
As Indonesia’s digital economy accelerates, the reliance on automated decision-making (ADM) for credit scoring has introduced a critical business vulnerability: **Systemic Bias.** This framework addresses the strategic necessity of auditing AI models to ensure that geographical variables and protected demographics (like age) do not serve as proxies for discriminatory lending. 

**The Strategic Challenge**
Current machine learning models, specifically those utilizing Alternative Data, often inadvertently penalize applicants from regions outside of Greater Jakarta (*Jabodetabek*) or specific demographic bands. This creates two primary risks:
1. **Regulatory Risk:** Non-compliance with **OJK Regulation No. 1/2026** and **UU PDP No. 27/2022**.
2. **Market Opportunity Loss:** Improperly rejecting credit-worthy individuals in emerging hubs like Medan, Surabaya, or IKN.

---

## The Business Case: Fairness as a Competitive Advantage

### 1. Market Expansion & Revenue Growth
**Financial inclusion is a multi-billion rupiah opportunity.** By identifying and correcting regional bias, FSTIs can safely approve high-potential borrowers in the "Outer Islands" who are currently being auto-rejected by legacy algorithms. This framework turns "lost leads" into "loyal customers."

### 2. Legal Uptime & Compliance
With the enforcement of **UU PDP Article 37**, Indonesian citizens now have the right to contest fully automated decisions. This framework provides the necessary **Audit Trail**, mathematical justification, and **Human-in-the-Loop (HITL)** workflows to ensure your automated lending remains legally protected against data subject contestations.

### 3. Institutional Trust & ESG Signaling
**Responsible AI** is a key metric for institutional investors. Adopting an automated, agentic fairness framework signals that the organization is managed with the strategic risk oversight required for long-term stability.

---

## 🏛 Core Architecture (V2.0: Agentic FinOps Pipeline)

The AFA framework operates across three distinct defense perimeters:

### 1. Regional Bias Engine (`bias_audit.py`)
A two-tier econometric engine designed to detect "Algorithmic Regionalism".
* **Tier 1 (Diagnostic):** Calculates raw Disparate Impact (DI). If the DI ratio falls below the 80% Four-Fifths threshold, it automatically triggers a Tier 2 review.
* **Tier 2 (Conditional Demographic Disparity - CDD):** Executes a Logistic Regression (`statsmodels`) controlling for localized macroeconomic variables (e.g., provincial inflation, regional GDP). This mathematically proves whether a localized rejection rate is due to actual market realities or algorithmic redlining.
* **Artifact:** Generates an OJK-ready `fairness_audit_report.pdf` combining visual metrics and statistical p-values.

### 2. Demographic Profiling Engine (`age_bias_audit.py`)
A multi-class auditor evaluating algorithmic treatment across age bands to ensure compliance with UU PDP restrictions on automated profiling.
* Establishes a statistical baseline (e.g., 25-35 year-old core professionals).
* Calculates isolated DI ratios for marginalized bands (e.g., Gen-Z, Seniors).

### 3. Agentic Orchestration Layer (`agent_ticketing.py`)
Closes the Human-in-the-Loop (HITL) gap by bridging risk diagnostics with engineering workflows.
* Acts as an autonomous AI agent that ingests failing compliance metrics.
* Automatically drafts highly structured, urgent Jira remediation tickets detailing the exact proxy violations.
* Assigns specific data science remediation tasks (e.g., SHAP value extraction, feature orthogonalization).

---

## Technical Methodology: The Math Behind the Audit

To identify bias, Tier 1 of this framework utilizes the **Disparate Impact (DI) Ratio**, an industry-standard metric for measuring fairness.

### The Formula
The ratio compares the probability of loan approval for the **unprivileged group** against the **privileged group**.

$$DI = \frac{Pr(Y=1 | Group=Unprivileged)}{Pr(Y=1 | Group=Privileged)}$$

### The 80% Threshold
Following the **Four-Fifths Rule**, any model with a DI ratio below **0.80** is flagged for "Immediate Corrective Action."

---

## Regulatory Mapping & Compliance

| Regulation | Relevance to AI Governance | Compliance Action |
| :--- | :--- | :--- |
| **UU PDP No. 27/2022** | Article 37: Right to contest ADM decisions (e.g. Age Profiling). | Execution of Multi-Class Demographic Audits (`age_bias_audit.py`). |
| **POJK 1/2026** | Mandates IT Risk Management & Algorithmic Transparency for FSTIs. | Tier 2 Logistic Regression to isolate algorithmic redlining (`bias_audit.py`). |
| **SE Kominfo 9/2023** | Principles of AI Inclusivity. | Continuous DI Ratio monitoring & reporting. |
| **Pancasila Sila 5** | Social Justice for all Indonesians. | Ensuring financial inclusion for the Archipelago. |

---

## ⚙️ Installation & Execution

### 1. Environment Setup
```powershell
git clone [https://github.com/johannesbambang/ID-Fintech-AI-Fairness.git](https://github.com/johannesbambang/ID-Fintech-AI-Fairness.git)
cd ID-Fintech-AI-Fairness
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install pandas numpy matplotlib statsmodels fpdf
