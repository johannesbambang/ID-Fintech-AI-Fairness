import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from fpdf import FPDF
import os
from datetime import datetime

def audit_regional_fairness(data, region_col, outcome_col, macro_control_cols=None, privileged_region='Java', export_pdf=True):
    """
    Executes a two-tier AI Fairness Audit for OJK 1/2026 Compliance.
    Tier 1: Calculates raw Disparate Impact (DI) Ratio.
    Tier 2: If DI < 0.80, executes Conditional Demographic Disparity (CDD) using Logistic Regression.
    
    Returns:
        tuple: (di_ratio, tier_1_verdict, tier_2_verdict, img_filename, pdf_filename)
    """
    print("--- OJK Compliance: AI Fairness Audit ---")
    print("[SYSTEM] Executing Tier 1: Disparate Impact Diagnostic...")
    
    # 1. TIER 1: Calculate Raw Rates
    privileged_apps = data[data[region_col] == privileged_region]
    privileged_rate = privileged_apps[outcome_col].mean()
    
    unprivileged_apps = data[data[region_col] != privileged_region]
    unprivileged_rate = unprivileged_apps[outcome_col].mean()
    
    di_ratio = unprivileged_rate / privileged_rate if privileged_rate > 0 else 0
    
    print(f"{privileged_region} Approval Rate: {privileged_rate:.2%}")
    print(f"Outer Island Approval Rate: {unprivileged_rate:.2%}")
    print(f"Disparate Impact Ratio: {di_ratio:.4f}")
    
    tier_1_verdict = "PASS"
    trigger_tier_2 = False
    
    if di_ratio < 0.8:
        print("STATUS: Tier 1 FAIL - Raw Bias Detected. Initiating Tier 2 (CDD)...")
        tier_1_verdict = "FAIL - HITL REVIEW REQUIRED"
        trigger_tier_2 = True
    else:
        print("STATUS: Tier 1 PASS - Model meets raw fairness thresholds.")

    # 2. TIER 2: Conditional Demographic Disparity (CDD)
    tier_2_verdict = "N/A"
    odds_ratio = None
    p_value = None
    
    if trigger_tier_2 and macro_control_cols:
        print(f"[SYSTEM] Controlling for: {macro_control_cols}")
        # Create binary target for protected region (1 = Outer Islands, 0 = Java)
        data['is_outer'] = (data[region_col] != privileged_region).astype(int)
        
        X_cols = ['is_outer'] + macro_control_cols
        X = sm.add_constant(data[X_cols])
        y = data[outcome_col]
        
        try:
            logit_model = sm.Logit(y, X)
            result = logit_model.fit(disp=0)
            
            regional_coef = result.params['is_outer']
            p_value = result.pvalues['is_outer']
            odds_ratio = np.exp(regional_coef)
            is_significant = p_value < 0.05
            
            if regional_coef < 0 and is_significant:
                tier_2_verdict = "FAIL - ISOLATED BIAS DETECTED"
                print(f"STATUS: Tier 2 FAIL - Penalty is statistically significant (p={p_value:.4f}).")
            else:
                tier_2_verdict = "PASS - DISPARITY EXPLAINED BY MACRO CONTROLS"
                print(f"STATUS: Tier 2 PASS - Disparity correlates with market realities, not region.")
                
        except Exception as e:
            tier_2_verdict = "ERROR - Model Convergence Failed"
            print(f"[ERROR] Tier 2 execution failed: {e}")

    # 3. Create Visualization with timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    img_filename = f"fairness_audit_{timestamp}.png"
    pdf_filename = f"fairness_audit_report_{timestamp}.pdf"
    
    regions = [privileged_region, 'Outer Islands']
    rates = [privileged_rate, unprivileged_rate]
    
    plt.figure(figsize=(8, 6))
    colors = ['#2ecc71', '#e74c3c' if di_ratio < 0.8 else '#3498db']
    plt.bar(regions, rates, color=colors)
    plt.axhline(y=privileged_rate * 0.8, color='black', linestyle='--', label='80% Fairness Threshold')
    
    plt.title('AI Lending Fairness Audit: Regional Approval Rates', fontsize=14)
    plt.ylabel('Approval Rate', fontsize=12)
    plt.ylim(0, 1)
    plt.legend()
    
    plt.savefig(img_filename)
    print(f"\nSUCCESS: Plot saved as '{img_filename}'")
    plt.close()

    # 4. Export PDF Report
    if export_pdf:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "OJK Compliance: AI Fairness Audit Report", ln=True, align="C")
        pdf.ln(5)
        
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Tier 1: Raw Disparate Impact (DI) Diagnostic", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 8, f"Privileged Region Baseline: {privileged_region}", ln=True)
        pdf.cell(0, 8, f"{privileged_region} Rate: {privileged_rate:.2%}", ln=True)
        pdf.cell(0, 8, f"Outer Islands Rate: {unprivileged_rate:.2%}", ln=True)
        pdf.cell(0, 8, f"Disparate Impact Ratio: {di_ratio:.4f}", ln=True)
        
        if di_ratio < 0.8:
            pdf.set_text_color(255, 0, 0)
        pdf.cell(0, 8, f"Tier 1 Verdict: {tier_1_verdict}", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)
        
        if trigger_tier_2 and macro_control_cols:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Tier 2: Conditional Demographic Disparity (CDD)", ln=True)
            pdf.set_font("Arial", "", 10)
            pdf.multi_cell(0, 6, f"Macroeconomic Controls Applied: {', '.join(macro_control_cols)}")
            pdf.set_font("Arial", "", 12)
            
            if odds_ratio is not None:
                pdf.cell(0, 8, f"Isolated Regional Odds Ratio: {odds_ratio:.4f}", ln=True)
                pdf.cell(0, 8, f"Statistical Significance (p-value): {p_value:.4f}", ln=True)
                
            if "FAIL" in tier_2_verdict:
                pdf.set_text_color(255, 0, 0)
            else:
                pdf.set_text_color(0, 128, 0)
            pdf.multi_cell(0, 8, f"Tier 2 Verdict: {tier_2_verdict}")
            pdf.set_text_color(0, 0, 0)
        
        # Add timestamp footer
        pdf.set_font("Arial", "I", 10)
        pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="R")
        
        pdf.image(img_filename, x=10, y=pdf.get_y() + 5, w=180)
        pdf.output(pdf_filename)
        print(f"SUCCESS: Comprehensive PDF report saved as '{pdf_filename}'")
    
    return di_ratio, tier_1_verdict, tier_2_verdict, img_filename, pdf_filename

if __name__ == "__main__":
    # Integration Point: Checking for local CSV file first
    data_path = 'loan_data_pilot.csv'
    
    if os.path.exists(data_path):
        print(f"[SYSTEM] Loading pilot data from {data_path}...")
        df = pd.read_csv(data_path)
    else:
        print(f"[SYSTEM] {data_path} not found. Running with high-fidelity simulated data.")
        np.random.seed(42)
        n_samples = 500
        regions = ['Java'] * 300 + ['Sumatra'] * 100 + ['Papua'] * 100
        inflation = [np.random.uniform(2.0, 3.5) if r == 'Java' else np.random.uniform(4.0, 6.0) for r in regions]
        gdp_growth = [np.random.uniform(4.5, 6.0) if r == 'Java' else np.random.uniform(2.0, 4.0) for r in regions]
        base_probs = [0.80 if r == 'Java' else 0.40 for r in regions]
        approvals = [np.random.binomial(1, p) for p in base_probs]

        df = pd.DataFrame({
            'region': regions,
            'provincial_inflation': inflation,
            'regional_gdp_growth': gdp_growth,
            'approved': approvals
        })
    
    di, tier1, tier2, img, pdf = audit_regional_fairness(
        data=df, 
        region_col='region', 
        outcome_col='approved', 
        macro_control_cols=['provincial_inflation', 'regional_gdp_growth']
    )
    
    print(f"\n--- Audit Summary ---")
    print(f"Disparate Impact Ratio: {di:.4f}")
    print(f"Tier 1 Verdict: {tier1}")
    print(f"Tier 2 Verdict: {tier2}")
    print(f"Output files: {img}, {pdf}")