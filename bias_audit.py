import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

def audit_regional_fairness(data, region_col, outcome_col, privileged_region='Java', export_pdf=True):
    """
    Calculates DI Ratio, generates visualization, and exports an OJK-compliant PDF report.
    """
    # 1. Calculate rates
    java_apps = data[data[region_col] == privileged_region]
    java_approval_rate = java_apps[outcome_col].mean()
    
    outer_apps = data[data[region_col] != privileged_region]
    outer_approval_rate = outer_apps[outcome_col].mean()
    
    di_ratio = outer_approval_rate / java_approval_rate
    
    # 2. Terminal report
    print("--- OJK Compliance: AI Fairness Audit ---")
    print(f"Java Approval Rate: {java_approval_rate:.2%}")
    print(f"Outer Island Approval Rate: {outer_approval_rate:.2%}")
    print(f"Disparate Impact Ratio: {di_ratio:.4f}")
    
    if di_ratio < 0.8:
        print("STATUS: FAIL - Significant Bias Detected.")
        print("ACTION: Model retraining and Tier 2 human review required.")
        verdict = "FAIL"
    else:
        print("STATUS: PASS - Model meets fairness thresholds.")
        verdict = "PASS"
    
    # 3. Create bar chart
    regions = [privileged_region, 'Outer Islands']
    rates = [java_approval_rate, outer_approval_rate]
    
    plt.figure(figsize=(8, 6))
    colors = ['#2ecc71', '#e74c3c' if di_ratio < 0.8 else '#3498db']
    plt.bar(regions, rates, color=colors)
    plt.axhline(y=java_approval_rate * 0.8, color='black', linestyle='--', label='80% Fairness Threshold')
    
    plt.title('AI Lending Fairness Audit: Regional Approval Rates', fontsize=14)
    plt.ylabel('Approval Rate', fontsize=12)
    plt.ylim(0, 1)
    plt.legend()
    
    plt.savefig('fairness_audit_result.png')
    print("\nSUCCESS: Plot saved as 'fairness_audit_result.png'")
    plt.close()  # Closes silently without throwing the interactive error
    
    # 4. Export PDF report
    if export_pdf:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "OJK Compliance: AI Fairness Audit Report", ln=True, align="C")
        pdf.ln(10)
        
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Privileged Region: {privileged_region}", ln=True)
        pdf.cell(0, 10, f"Java Approval Rate: {java_approval_rate:.2%}", ln=True)
        pdf.cell(0, 10, f"Outer Islands Approval Rate: {outer_approval_rate:.2%}", ln=True)
        pdf.cell(0, 10, f"Disparate Impact Ratio: {di_ratio:.4f}", ln=True)
        pdf.cell(0, 10, f"Verdict: {verdict}", ln=True)
        pdf.ln(5)
        
        if di_ratio < 0.8:
            pdf.set_text_color(255, 0, 0)
            pdf.cell(0, 10, "Action Required: Model retraining and Tier 2 human review.", ln=True)
            pdf.set_text_color(0, 0, 0)
        
        # Add the chart image to the PDF
        pdf.image('fairness_audit_result.png', x=10, y=pdf.get_y(), w=190)
        
        pdf.output("fairness_audit_report.pdf")
        print("SUCCESS: PDF report saved as 'fairness_audit_report.pdf'")
    
    return di_ratio, verdict

if __name__ == "__main__":
    # Sample data
    df = pd.DataFrame({
        'region': ['Java']*100 + ['Sumatra']*50 + ['Papua']*50,
        'approved': [1]*85 + [0]*15 + [1]*60 + [0]*40
    })
    
    # Run audit and generate PDF
    audit_regional_fairness(df, 'region', 'approved', export_pdf=True)
