import streamlit as st
from pathlib import Path

COLORS = {
    'primary': '#1f77b4',
    'success': '#2ca02c',
    'warning': '#ff7f0e',
    'danger': '#d62728',
    'dark_danger': '#8b0000',
    'background': '#f0f2f6',
    'text': '#262730',
    'border': '#e0e0e0',
}

RISK_LEVELS = {
    'LOW': {'range': (0, 0.3), 'color': COLORS['success'], 'icon': '🟢', 'action': 'RECOMMEND APPROVAL'},
    'MEDIUM': {'range': (0.3, 0.5), 'color': COLORS['warning'], 'icon': '🟡', 'action': 'PROCEED WITH CAUTION'},
    'HIGH': {'range': (0.5, 0.7), 'color': COLORS['danger'], 'icon': '🟠', 'action': 'REQUEST MORE DOCUMENTATION'},
    'VERY_HIGH': {'range': (0.7, 1.0), 'color': COLORS['dark_danger'], 'icon': '🔴', 'action': 'RECOMMEND DECLINE'},
}

FEATURE_CONFIG = {
    'numeric': {
        'Age': {'min_value': 18, 'max_value': 100, 'value': 35, 'step': 1},
        'Income': {'min_value': 20000, 'max_value': 500000, 'value': 75000, 'step': 5000},
        'LoanAmount': {'min_value': 50000, 'max_value': 1000000, 'value': 250000, 'step': 10000},
        'CreditScore': {'min_value': 300, 'max_value': 850, 'value': 720, 'step': 10},
        'MonthsEmployed': {'min_value': 0, 'max_value': 600, 'value': 120, 'step': 1},
        'NumCreditLines': {'min_value': 0, 'max_value': 30, 'value': 5, 'step': 1},
        'InterestRate': {'min_value': 1.0, 'max_value': 20.0, 'value': 5.5, 'step': 0.1},
        'LoanTerm': {'min_value': 12, 'max_value': 480, 'value': 360, 'step': 12},
        'DTIRatio': {'min_value': 0.0, 'max_value': 1.0, 'value': 0.35, 'step': 0.05},
    },
    'categorical': {
        'Education': {'options': [1, 2, 3], 'labels': ['High School', "Bachelor's", "Master's"], 'default': 1},
        'EmploymentType': {'options': [0, 1], 'labels': ['Self-Employed', 'Salaried'], 'default': 1},
        'MaritalStatus': {'options': [0, 1], 'labels': ['Single', 'Married'], 'default': 0},
        'HasMortgage': {'options': [0, 1], 'labels': ['No', 'Yes'], 'default': 0},
        'HasDependents': {'options': [0, 1], 'labels': ['No', 'Yes'], 'default': 0},
        'LoanPurpose': {'options': [0, 1, 2], 'labels': ['Auto', 'Home', 'Personal'], 'default': 0},
        'HasCoSigner': {'options': [0, 1], 'labels': ['No', 'Yes'], 'default': 0},
    },
}

PAGE_ICONS = {
    'prediction': '📊',
    'batch': '📈',
    'info': 'ℹ️',
}

MODEL_PATHS = {
    'primary': 'models/loan_default_model.pkl',
    'fallback': 'models/loan_model.pkl',
}

DATASET_INFO = {
    'total_records': 255347,
    'train_split': 0.8,
    'features': 17,
    'target': 'Default',
}

def get_model_path():
    project_root = Path(__file__).parent.parent.parent
    for path in [MODEL_PATHS['primary'], MODEL_PATHS['fallback']]:
        full_path = project_root / path
        if full_path.exists():
            return full_path
    return None
