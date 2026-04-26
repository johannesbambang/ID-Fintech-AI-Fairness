import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

def audit_age_fairness(data: pd.DataFrame, 
                       age_col: str, 
                       outcome_col: str, 
                       reference_group: str = '25-35') -> pd.DataFrame:
    """
    Executes an AI Fairness Audit for Age-based algorithmic profiling.
    Ensures compliance with UU PDP No. 27/2022 regarding automated decision-making.
    """
    
    print("--- UU PDP No. 27/2022 Compliance: Age Bias Audit ---")
    print(f"[SYSTEM] Establishing Reference Group Baseline: {reference_group}")
    
    # 1. Calculate the baseline approval rate for the reference group
    try:
        ref_data = data[data[age_col] == reference_group]
        ref_approval_rate = ref_data[outcome_col].mean()
    except Exception as e:
        print(f"[ERROR] Reference group '{reference_group}' not found in data.")
        return None

    print(f"Baseline Approval Rate ({reference_group}): {ref_approval_rate:.2%}\n")
    
    # 2. Calculate group-specific DI Ratios
    results = []
    age_groups = sorted(data[age_col].unique())
    
    for group in age_groups:
        group_data = data[data[age_col] == group]
        group_rate = group_data[outcome_col].mean()
        
        # Calculate Disparate Impact (DI) Ratio
        di_ratio = group_rate / ref_approval_rate if ref_approval_rate > 0 else 0
        
        # Determine Status (OJK/UU PDP 80% Rule)
        if group == reference_group:
            status = "BASELINE"
        elif di_ratio < 0.80:
            status = "FAIL (Bias Detected)"
        else:
            status = "PASS"
            
        results.append({
            "Age_Group": group,
            "Approval_Rate": f"{group_rate:.2%}",
            "DI_Ratio": f"{di_ratio:.4f}",
            "Status": status
        })
        print(f"Group: {group:<7} | Rate: {group_rate:.2%} | DI: {di_ratio:.4f} | Status: {status}")

    # 3. Create Visualization with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    img_filename = f"age_bias_audit_{timestamp}.png"

    results_df = pd.DataFrame(results)
    
    plt.figure(figsize=(10, 6))
    colors = ['#3498db' if s == "PASS" else '#e74c3c' if s == "FAIL (Bias Detected)" else '#2ecc71' for s in results_df['Status']]
    
    plt.bar(results_df['Age_Group'], [float(x.strip('%'))/100 for x in results_df['Approval_Rate']], color=colors)
    plt.axhline(y=ref_approval_rate, color='black', linestyle='-', label=f'Baseline ({reference_group})')
    plt.axhline(y=ref_approval_rate * 0.8, color='red', linestyle='--', label='80% Fairness Threshold')
    
    plt.title(f'AI Lending Fairness Audit: Age-Based Profiling ({timestamp})', fontsize=14)
    plt.ylabel('Approval Rate', fontsize=12)
    plt.xlabel('Applicant Age Band', fontsize=12)
    plt.ylim(0, 1)
    plt.legend()
    
    plt.savefig(img_filename)
    print(f"\nSUCCESS: Multi-class plot saved as '{img_filename}'")
    plt.close()
    
    return results_df

if __name__ == "__main__":
    # Integration Point: Ingest the same pilot data as bias_audit.py
    data_path = 'loan_data_pilot.csv'
    
    if os.path.exists(data_path):
        print(f"[SYSTEM] Loading pilot data from {data_path}...")
        df = pd.read_csv(data_path)
    else:
        print(f"[SYSTEM] {data_path} not found. Running with high-fidelity simulated data.")
        np.random.seed(42)
        n_samples = 1000
        age_bands = ['18-24', '25-35', '36-45', '46-60', '60+']
        # Mocking specific bias: baseline high for 25-45, penalizing young and old
        probs = [0.35, 0.85, 0.80, 0.65, 0.40] 
        mock_ages = np.random.choice(age_bands, n_samples)
        mock_approvals = [np.random.binomial(1, probs[age_bands.index(age)]) for age in mock_ages]
        df = pd.DataFrame({'age_band': mock_ages, 'approved': mock_approvals})
    
    audit_age_fairness(df, 'age_band', 'approved')