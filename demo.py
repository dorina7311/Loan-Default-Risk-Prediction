import sys
from pathlib import Path
import pandas as pd
from src.predict import LoanDefaultPredictor

project_root = Path(__file__).parent

def print_header():
    print("\n" + "="*70)
    print("LOAN DEFAULT RISK PREDICTION SYSTEM")
    print("="*70)
    print("\nThis system predicts whether a borrower will default on their loan.")
    print("It analyzes borrower characteristics and provides a risk assessment.\n")

def print_feature_info():
    print("\n" + "-"*70)
    print("BORROWER INFORMATION REQUIRED:")
    print("-"*70)
    features = {
        "Age": "Age of borrower (years)",
        "Income": "Annual income (USD)",
        "LoanAmount": "Amount of loan requested (USD)",
        "CreditScore": "Credit score (300-850)",
        "MonthsEmployed": "Months employed at current job",
        "NumCreditLines": "Number of active credit lines",
        "InterestRate": "Interest rate on loan (%)",
        "LoanTerm": "Length of loan (months)",
        "DTIRatio": "Debt-to-Income ratio (0.0-1.0)",
        "Education": "Education level (1=HS, 2=Bachelor, 3=Master)",
        "EmploymentType": "Employment type (0=Self-employed, 1=Salaried)",
        "MaritalStatus": "Marital status (0=Single, 1=Married)",
        "HasMortgage": "Has mortgage (0=No, 1=Yes)",
        "HasDependents": "Has dependents (0=No, 1=Yes)",
        "LoanPurpose": "Loan purpose (0=Auto, 1=Home, 2=Personal)",
        "HasCoSigner": "Has co-signer (0=No, 1=Yes)"
    }
    
    for i, (feature, desc) in enumerate(features.items(), 1):
        print(f"{i:2d}. {feature:20s} - {desc}")

def get_sample_borrower():
    return {
        'Age': 35,
        'Income': 75000,
        'LoanAmount': 250000,
        'CreditScore': 720,
        'MonthsEmployed': 120,
        'NumCreditLines': 5,
        'InterestRate': 5.5,
        'LoanTerm': 360,
        'DTIRatio': 0.35,
        'Education': 2,
        'EmploymentType': 1,
        'MaritalStatus': 0,
        'HasMortgage': 1,
        'HasDependents': 0,
        'LoanPurpose': 0,
        'HasCoSigner': 0
    }

def get_high_risk_borrower():
    return {
        'Age': 28,
        'Income': 35000,
        'LoanAmount': 300000,
        'CreditScore': 580,
        'MonthsEmployed': 6,
        'NumCreditLines': 12,
        'InterestRate': 9.5,
        'LoanTerm': 360,
        'DTIRatio': 0.72,
        'Education': 1,
        'EmploymentType': 0,
        'MaritalStatus': 0,
        'HasMortgage': 0,
        'HasDependents': 2,
        'LoanPurpose': 2,
        'HasCoSigner': 0
    }

def get_low_risk_borrower():
    return {
        'Age': 50,
        'Income': 150000,
        'LoanAmount': 300000,
        'CreditScore': 800,
        'MonthsEmployed': 300,
        'NumCreditLines': 3,
        'InterestRate': 3.5,
        'LoanTerm': 240,
        'DTIRatio': 0.20,
        'Education': 3,
        'EmploymentType': 1,
        'MaritalStatus': 1,
        'HasMortgage': 1,
        'HasDependents': 1,
        'LoanPurpose': 1,
        'HasCoSigner': 0
    }

def predict_and_display(predictor, borrower, description):
    print(f"\n{'='*70}")
    print(f"SCENARIO: {description}")
    print(f"{'='*70}")
    
    print("\nBORROWER PROFILE:")
    print("-" * 70)
    for key, value in borrower.items():
        if key in ['Income', 'LoanAmount']:
            print(f"  {key:20s}: ${value:,.0f}")
        elif key in ['DTIRatio', 'InterestRate']:
            print(f"  {key:20s}: {value:.2f}")
        else:
            print(f"  {key:20s}: {value}")
    
    print("\nANALYZING WITH AI MODEL...")
    try:
        result = predictor.predict_single(borrower)
    except Exception as e:
        print(f"\nError during prediction: {str(e)}")
        print("Please check your input values are within valid ranges.")
        return None
    
    print("\n" + "="*70)
    print("PREDICTION RESULT:")
    print("="*70)
    
    prediction = result['prediction_label']
    prob_default = result['probability_default']
    prob_no_default = result['probability_no_default']
    
    if prediction == 'Default':
        print(f"\nRISK LEVEL: HIGH - LIKELY TO DEFAULT")
    else:
        print(f"\nRISK LEVEL: LOW - LIKELY TO REPAY")
    
    print(f"\n  Probability of DEFAULT:     {prob_default:>7.2%}")
    print(f"  Probability of NO DEFAULT:  {prob_no_default:>7.2%}")
    
    print("\nRISK ASSESSMENT:")
    if prob_default > 0.7:
        print("    VERY HIGH RISK - RECOMMEND DECLINE")
    elif prob_default > 0.5:
        print("    HIGH RISK - REQUEST MORE DOCUMENTATION")
    elif prob_default > 0.3:
        print("    MEDIUM RISK - PROCEED WITH CAUTION")
    else:
        print("    LOW RISK - RECOMMEND APPROVAL")
    
    return result

def validate_input(feature, value):
    """Validate input value for a given feature."""
    validations = {
        'Age': (18, 80, "Age must be between 18 and 80"),
        'Income': (100, None, "Income must be between $100 and has no limit"),
        'LoanAmount': (100, None, "Loan amount must be at least $50,000"),
        'CreditScore': (300, 850, "Credit score must be between 300 and 850"),
        'MonthsEmployed': (1, 600, "Months employed must be between 1 and 600"),
        'NumCreditLines': (0, 20, "Number of credit lines must be between 0 and 20"),
        'InterestRate': (2.0, 10.0, "Interest rate must be between 2% and 10%"),
        'LoanTerm': (60, 360, "Loan term must be between 60 and 360 months"),
        'DTIRatio': (0.0, 0.75, "Debt-to-Income ratio must be between 0.0 and 0.75"),
        'Education': (1, 3, "Education level must be 1 (HS), 2 (Bachelor), or 3 (Master)"),
        'EmploymentType': (0, 1, "Employment type must be 0 (Self) or 1 (Salaried)"),
        'MaritalStatus': (0, 1, "Marital status must be 0 (Single) or 1 (Married)"),
        'HasMortgage': (0, 1, "Has mortgage must be 0 (No) or 1 (Yes)"),
        'HasDependents': (0, 1, "Has dependents must be 0 (No) or 1 (Yes)"),
        'LoanPurpose': (0, 2, "Loan purpose must be 0 (Auto), 1 (Home), or 2 (Personal)"),
        'HasCoSigner': (0, 1, "Has co-signer must be 0 (No) or 1 (Yes)"),
    }
    
    if feature in validations:
        min_val, max_val, msg = validations[feature]
        if value < min_val:
            return False, msg
        if max_val is not None and value > max_val:
            return False, msg
    
    return True, "Valid"

def interactive_mode(predictor):
    print(f"\n{'='*70}")
    print("INTERACTIVE MODE - ENTER CUSTOM BORROWER DATA")
    print(f"{'='*70}")
    
    borrower = {}
    features = {
        'Age': ('int', "Age of borrower (years): "),
        'Income': ('float', "Annual income (USD): "),
        'LoanAmount': ('float', "Loan amount requested (USD): "),
        'CreditScore': ('int', "Credit score (300-850): "),
        'MonthsEmployed': ('int', "Months employed at current job: "),
        'NumCreditLines': ('int', "Number of active credit lines: "),
        'InterestRate': ('float', "Interest rate (%): "),
        'LoanTerm': ('int', "Loan term (months): "),
        'DTIRatio': ('float', "Debt-to-Income ratio (0-1): "),
        'Education': ('int', "Education level (1=HS, 2=Bachelor, 3=Master): "),
        'EmploymentType': ('int', "Employment type (0=Self, 1=Salaried): "),
        'MaritalStatus': ('int', "Marital status (0=Single, 1=Married): "),
        'HasMortgage': ('int', "Has mortgage? (0=No, 1=Yes): "),
        'HasDependents': ('int', "Has dependents? (0=No, 1=Yes): "),
        'LoanPurpose': ('int', "Loan purpose (0=Auto, 1=Home, 2=Personal): "),
        'HasCoSigner': ('int', "Has co-signer? (0=No, 1=Yes): "),
    }
    
    try:
        for feature, (dtype, prompt) in features.items():
            while True:
                try:
                    value = input(f"  {prompt}")
                    if dtype == 'int':
                        value = int(value)
                    else:
                        value = float(value)
                    
                    is_valid, msg = validate_input(feature, value)
                    if not is_valid:
                        print(f"    Error: {msg}")
                        continue
                    
                    borrower[feature] = value
                    break
                except ValueError:
                    print(f"    Error: Invalid input. Please enter a valid {dtype}.")
        
        predict_and_display(predictor, borrower, "Custom Borrower Data")
        return True
    except KeyboardInterrupt:
        print("\n\nInput cancelled.")
        return False

def main():
    print_header()
    
    model_path = project_root / "models" / "loan_default_model.pkl"
    
    try:
        print("Loading trained model...")
        predictor = LoanDefaultPredictor(str(model_path))
        print("Model loaded successfully!\n")
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        print("\nMake sure you have run: python src/train_model.py")
        return
    
    while True:
        print("\n" + "="*70)
        print("MAIN MENU - CHOOSE AN OPTION:")
        print("="*70)
        print("\n1. View Low-Risk Borrower (Good credit, high income)")
        print("2. View High-Risk Borrower (Poor credit, low income)")
        print("3. View Medium-Risk Borrower (Average profile)")
        print("4. Enter Custom Borrower Data")
        print("5. View Feature Information")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            predict_and_display(predictor, get_low_risk_borrower(), 
                              "Low-Risk Borrower - Likely Approval")
        
        elif choice == '2':
            predict_and_display(predictor, get_high_risk_borrower(), 
                              "High-Risk Borrower - Likely Decline")
        
        elif choice == '3':
            predict_and_display(predictor, get_sample_borrower(), 
                              "Medium-Risk Borrower - Likely Approval")
        
        elif choice == '4':
            if not interactive_mode(predictor):
                continue
        
        elif choice == '5':
            print_feature_info()
        
        elif choice == '6':
            print("\n" + "="*70)
            print("Thank you for using the Loan Default Prediction System!")
            print("="*70 + "\n")
            break
        
        else:
            print("\nInvalid choice. Please enter 1-6.")

if __name__ == "__main__":
    main()
