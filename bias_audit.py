import pandas as pd

def audit_regional_fairness(data, region_col, outcome_col, privileged_region='Java'):
    """
    Calculates the Disparate Impact (DI) Ratio to detect regional bias.
    Aligned with OJK 1/2026 and UU PDP fairness principles.
    """
    # 1. Calculate Approval Rate for Java (Privileged)
    java_apps = data[data[region_col] == privileged_region]
    java_approval_rate = java_apps[outcome_col].mean()

    # 2. Calculate Approval Rate for Outer Islands (Unprivileged)
    outer_apps = data[data[region_col] != privileged_region]
    outer_approval_rate = outer_apps[outcome_col].mean()

    # 3. Compute Disparate Impact Ratio
    di_ratio = outer_approval_rate / java_approval_rate

    print("--- OJK Compliance: AI Fairness Audit ---")
    print(f"Java Approval Rate: {java_approval_rate:.2%}")
    print(f"Outer Island Approval Rate: {outer_approval_rate:.2%}")
    print(f"Disparate Impact Ratio: {di_ratio:.4f}")

    # 4. Apply the 80% Rule (Four-Fifths Rule)
    if di_ratio < 0.8:
        print("STATUS: FAIL - Significant Bias Detected.")
        print("ACTION: Model retraining and Tier 2 human review required.")
    else:
        print("STATUS: PASS - Model meets fairness thresholds.")

# Example Usage with Hypothetical Indonesian Data
if __name__ == "__main__":
    # Sample Data: 1 = Approved, 0 = Rejected
    df = pd.DataFrame({
        'region': ['Java']*100 + ['Sumatra']*50 + ['Papua']*50,
        'approved': [1]*85 + [0]*15 + [1]*60 + [0]*40  # 85% vs 60%
    })
    
    audit_regional_fairness(df, 'region', 'approved')
