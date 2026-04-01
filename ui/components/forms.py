import streamlit as st
from ui.config.settings import FEATURE_CONFIG

def render_numeric_inputs(col1, col2):
    numeric_config = FEATURE_CONFIG['numeric']
    
    with col1:
        age = st.number_input("Age (years)", **numeric_config['Age'])
        income = st.number_input("Annual Income ($)", **numeric_config['Income'])
        loan_amount = st.number_input("Loan Amount ($)", **numeric_config['LoanAmount'])
        credit_score = st.number_input("Credit Score", **numeric_config['CreditScore'])
        months_employed = st.number_input("Months Employed", **numeric_config['MonthsEmployed'])
    
    with col2:
        num_credit_lines = st.number_input("Number of Credit Lines", **numeric_config['NumCreditLines'])
        interest_rate = st.number_input("Interest Rate (%)", **numeric_config['InterestRate'])
        loan_term = st.number_input("Loan Term (months)", **numeric_config['LoanTerm'])
        dti_ratio = st.number_input("Debt-to-Income Ratio", **numeric_config['DTIRatio'])
    
    return {
        'Age': age, 'Income': income, 'LoanAmount': loan_amount,
        'CreditScore': credit_score, 'MonthsEmployed': months_employed,
        'NumCreditLines': num_credit_lines, 'InterestRate': interest_rate,
        'LoanTerm': loan_term, 'DTIRatio': dti_ratio
    }

def render_categorical_inputs(col1, col2):
    categorical_config = FEATURE_CONFIG['categorical']
    
    with col1:
        education_idx = st.selectbox(
            "Education Level",
            range(len(categorical_config['Education']['options'])),
            format_func=lambda x: categorical_config['Education']['labels'][x],
            index=1
        )
        employment_idx = st.selectbox(
            "Employment Type",
            range(len(categorical_config['EmploymentType']['options'])),
            format_func=lambda x: categorical_config['EmploymentType']['labels'][x],
            index=1
        )
        marital_idx = st.selectbox(
            "Marital Status",
            range(len(categorical_config['MaritalStatus']['options'])),
            format_func=lambda x: categorical_config['MaritalStatus']['labels'][x],
            index=0
        )
        st.markdown("<div style='margin-top: -18px; margin-bottom: 8px;'><span style='color: #000000; font-weight: 700; font-size: 14px;'>Has Co-Signer?</span></div>", unsafe_allow_html=True)
        has_cosigner_idx = st.selectbox(
            "",
            range(len(categorical_config['HasCoSigner']['options'])),
            format_func=lambda x: categorical_config['HasCoSigner']['labels'][x],
            index=0,
            key="cosigner_input",
            label_visibility="collapsed"
        )
    
    with col2:
        mortgage_idx = st.selectbox(
            "Has Mortgage?",
            range(len(categorical_config['HasMortgage']['options'])),
            format_func=lambda x: categorical_config['HasMortgage']['labels'][x],
            index=0
        )
        dependents_idx = st.selectbox(
            "Has Dependents?",
            range(len(categorical_config['HasDependents']['options'])),
            format_func=lambda x: categorical_config['HasDependents']['labels'][x],
            index=0
        )
        loan_purpose_idx = st.selectbox(
            "Loan Purpose",
            range(len(categorical_config['LoanPurpose']['options'])),
            format_func=lambda x: categorical_config['LoanPurpose']['labels'][x],
            index=0
        )
    
    return {
        'Education': categorical_config['Education']['options'][education_idx],
        'EmploymentType': categorical_config['EmploymentType']['options'][employment_idx],
        'MaritalStatus': categorical_config['MaritalStatus']['options'][marital_idx],
        'HasMortgage': categorical_config['HasMortgage']['options'][mortgage_idx],
        'HasDependents': categorical_config['HasDependents']['options'][dependents_idx],
        'LoanPurpose': categorical_config['LoanPurpose']['options'][loan_purpose_idx],
        'HasCoSigner': categorical_config['HasCoSigner']['options'][has_cosigner_idx],
    }

def build_borrower_form():
    with st.form("borrower_form", border=True):
        col1, col2 = st.columns(2, gap="medium")
        numeric_data = render_numeric_inputs(col1, col2)
        
        st.markdown("---")
        
        col3, col4 = st.columns(2, gap="medium")
        categorical_data = render_categorical_inputs(col3, col4)
        
        submitted = st.form_submit_button("🔍 Predict Risk", use_container_width=True)
        
        return {**numeric_data, **categorical_data}, submitted
