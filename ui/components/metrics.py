import streamlit as st
import pandas as pd
from ui.utils.formatters import format_currency, format_percentage
from ui.config.settings import FEATURE_CONFIG

def render_result_metrics(prob_default: float, prob_no_default: float, model_name: str):
    # Apply enhanced styling for metric boxes - prevent text truncation and ellipsis
    st.markdown("""
    <style>
    /* Metric box styling */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #f0f4f8 0%, #d8e6f3 100%) !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        border-left: 5px solid #1f77b4 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
        min-height: 120px !important;
    }
    
    /* All text inside metric box - no truncation */
    [data-testid="stMetric"] * {
        color: #000000 !important;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
    }
    
    /* Metric label styling */
    [data-testid="stMetric"] [data-testid="metric-label"] {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #1f3a56 !important;
        margin-bottom: 0.75rem !important;
        line-height: 1.4 !important;
    }
    
    /* Metric value styling */
    [data-testid="stMetric"] [data-testid="metric-value"] {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #000000 !important;
        line-height: 1.2 !important;
    }
    
    /* Metric delta styling */
    [data-testid="stMetric"] [data-testid="metric-delta"] {
        font-size: 12px !important;
        color: #1f3a56 !important;
    }
    
    /* Container for metric columns */
    [data-testid="column"] {
        overflow: visible !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.metric(
            label="📊 Default Probability",
            value=f"{prob_default:.1%}",
            help="Probability that borrower will default on loan"
        )
    
    with col2:
        st.metric(
            label="✅ No Default Probability",
            value=f"{prob_no_default:.1%}",
            help="Probability that borrower will successfully repay"
        )
    
    with col3:
        st.metric(
            label="🤖 Model Used",
            value=model_name,
            help="Machine learning model used for prediction"
        )

def render_borrower_summary(features: dict):
    """Display borrower summary with human-readable values"""
    with st.expander("📋 Borrower Profile Summary", expanded=False):
        # Create human-readable summary
        summary_data = []
        
        for key, value in features.items():
            # Format numeric values
            if key == 'Income':
                display_value = f"${value:,.0f}/year"
            elif key == 'LoanAmount':
                display_value = f"${value:,.0f}"
            elif key == 'InterestRate':
                display_value = f"{value:.1f}%"
            elif key == 'DTIRatio':
                display_value = f"{value:.2f}"
            elif key == 'Age':
                display_value = f"{value} years"
            elif key == 'MonthsEmployed':
                # Convert months to years and months
                years = value // 12
                months = value % 12
                display_value = f"{int(years)}y {int(months)}mo" if years > 0 else f"{int(months)}mo"
            elif key == 'LoanTerm':
                years = value // 12
                display_value = f"{int(years)} years ({int(value)} months)"
            elif key == 'CreditScore':
                display_value = f"{value} (Scale: 300-850)"
            elif key == 'NumCreditLines':
                display_value = f"{value} active lines"
            # Format categorical values using config
            elif key in FEATURE_CONFIG['categorical']:
                cat_config = FEATURE_CONFIG['categorical'][key]
                try:
                    idx = cat_config['options'].index(value)
                    display_value = cat_config['labels'][idx]
                except (ValueError, IndexError, KeyError) as e:
                    display_value = str(value)
            else:
                display_value = str(value)
            
            summary_data.append({
                'Field': key,
                'Value': display_value
            })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

def render_feature_table():
    features_info = {
        "Age": "Borrower age in years",
        "Income": "Annual income in USD",
        "LoanAmount": "Requested loan amount",
        "CreditScore": "Credit score (300-850)",
        "MonthsEmployed": "Current employment duration",
        "NumCreditLines": "Active credit lines",
        "InterestRate": "Loan interest rate in %",
        "LoanTerm": "Loan duration in months",
        "DTIRatio": "Debt-to-income ratio",
        "Education": "Education level (1-3)",
        "EmploymentType": "Employment classification",
        "MaritalStatus": "Marital status",
        "HasMortgage": "Mortgage ownership status",
        "HasDependents": "Dependent status",
        "LoanPurpose": "Loan purpose category",
        "HasCoSigner": "Co-signer availability",
    }
    
    df = pd.DataFrame({
        'Feature': list(features_info.keys()),
        'Description': list(features_info.values())
    })
    st.dataframe(df, use_container_width=True, hide_index=True)

def render_risk_guidelines():
    guidelines = {
        'Risk Level': ['🟢 Low Risk', '🟡 Medium Risk', '🟠 High Risk', '🔴 Very High Risk'],
        'Probability Range': ['0-30%', '30-50%', '50-70%', '70-100%'],
        'Recommended Action': ['Approve', 'Review', 'Additional Docs', 'Decline'],
    }
    
    st.dataframe(pd.DataFrame(guidelines), use_container_width=True, hide_index=True)
