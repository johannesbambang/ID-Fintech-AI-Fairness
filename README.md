# ID-Fintech-AI-Fairness

A strategic framework and Python-based audit tool for detecting regional bias in Indonesian Fintech lending, ensuring compliance with **OJK 1/2026** and **UU PDP**.

---

# Executive Summary: Mitigating Algorithmic Regionalism
### *A Strategic Framework for OJK-Compliant AI in Indonesian Fintech*

**Overview**
As Indonesia’s digital economy accelerates, the reliance on automated decision-making (ADM) for credit scoring has introduced a critical business vulnerability: **Systemic Regional Bias.** This framework addresses the strategic necessity of auditing AI models to ensure that geographical variables do not serve as proxies for discriminatory lending. By implementing a rigorous fairness audit, financial institutions can fulfill the mandates of **UU Pelindungan Data Pribadi (UU PDP)** while expanding their market share in under-banked provinces.

**The Strategic Challenge**
Current machine learning models, specifically those utilizing Alternative Data, often inadvertently penalize applicants from regions outside of the Greater Jakarta area (*Jabodetabek*). This "Regionalism" creates two primary risks:
1. **Regulatory Risk:** Non-compliance with **OJK Regulation No. 1/2026**.
2. **Market Opportunity Loss:** Improperly rejecting credit-worthy individuals in emerging hubs like Medan, Surabaya, or IKN.

---

# The Business Case: Fairness as a Competitive Advantage

### 1. Market Expansion & Revenue Growth
**Financial inclusion is a multi-billion rupiah opportunity.** By identifying and correcting regional bias, FSTIs can safely approve high-potential borrowers in the "Outer Islands" who are currently being auto-rejected by legacy algorithms. This framework turns "lost leads" into "loyal customers."

### 2. Legal Uptime & Compliance
With the enforcement of **UU PDP Article 37**, Indonesian citizens now have the right to contest fully automated decisions. This framework provides the necessary **Audit Trail** and **Human-in-the-Loop (HITL)** workflows to ensure your automated lending remains legally protected.

### 3. Institutional Trust & ESG Signaling
In the 2026 investment landscape, **Responsible AI** is a key metric for institutional investors. Adopting a transparent fairness framework signals that the organization is managed with the strategic foresight required for long-term stability.

---

# Technical Methodology: The Disparate Impact (DI) Audit

To identify regional bias, this framework utilizes the **Disparate Impact (DI) Ratio**, an industry-standard metric for measuring fairness.

### The Formula
The ratio compares the probability of loan approval for the **unprivileged group** (Outer Islands) against the **privileged group** (Java/Jabodetabek).

$$DI = \frac{Pr(Y=1 | Group=Unprivileged)}{Pr(Y=1 | Group=Privileged)}$$

### The 80% Threshold
Following the **Four-Fifths Rule**, any model with a DI ratio below **0.80** is flagged for "Immediate Corrective Action."

---

# Regulatory Mapping & Compliance

| Regulation | Relevance to AI Governance | Compliance Action |
| :--- | :--- | :--- |
| **UU PDP No. 27/2022** | Article 37: Right to contest ADM decisions. | Implement Tier 2 Human-in-the-loop review. |
| **POJK 1/2026** | Mandates IT Risk Management for FSTIs. | Continuous DI Ratio monitoring & reporting. |
| **SE Kominfo 9/2023** | Principles of AI Inclusivity. | Auditing for Regional/Geographic bias. |
| **Pancasila Sila 5** | Social Justice for all Indonesians. | Ensuring inclusion for the Archipelago. |

---

# About the Author
**Johannes Bambang Wirawan, MBA, MScFE**
*IT Helpdesk Supervisor | Quantitative Finance & Robotics Enthusiast*

* **MSc in Financial Engineering** - WorldQuant University (SK Equivalency Issued)
* **Executive MBA** - Valar Institute
* **B.A. in English Literature** - Binus University
* **Professional Master's in Robotics** - TECH Global University (In Progress)
