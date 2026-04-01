import streamlit as st
from pathlib import Path
from src.predict import LoanDefaultPredictor
import logging

logger = logging.getLogger(__name__)

@st.cache_resource
def initialize_model(model_path):
    """
    Load and cache the ML model for predictions.
    
    Args:
        model_path: Path to the saved model file
        
    Returns:
        LoanDefaultPredictor instance
        
    Raises:
        FileNotFoundError: If model file doesn't exist
        Exception: If model loading fails
    """
    try:
        logger.info(f"Loading model from: {model_path}")
        predictor = LoanDefaultPredictor(str(model_path))
        logger.info(f"Model loaded successfully: {predictor.model_name}")
        return predictor
    except FileNotFoundError as e:
        logger.error(f"Model file not found: {model_path}")
        raise
    except Exception as e:
        logger.error(f"Model loading failed: {str(e)}")
        raise

def validate_borrower_data(data: dict) -> tuple[bool, str]:
    """
    Validate borrower data before prediction.
    
    Args:
        data: Dictionary containing borrower features
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    numeric_fields = ['Age', 'Income', 'LoanAmount', 'CreditScore', 'MonthsEmployed', 
                     'NumCreditLines', 'InterestRate', 'LoanTerm', 'DTIRatio']
    
    for field in numeric_fields:
        if field not in data or data[field] is None:
            return False, f"Missing field: {field}"
    
    if not (18 <= data['Age'] <= 100):
        return False, "Age must be between 18 and 100"
    
    if data['DTIRatio'] < 0 or data['DTIRatio'] > 1:
        return False, "DTI Ratio must be between 0 and 1"
    
    if data['CreditScore'] < 300 or data['CreditScore'] > 850:
        return False, "Credit Score must be between 300 and 850"
    
    if data['Income'] < 0 or data['LoanAmount'] < 0:
        return False, "Income and Loan Amount must be positive"
    
    if data['InterestRate'] < 0 or data['InterestRate'] > 20:
        return False, "Interest Rate must be between 0 and 20%"
    
    logger.info("Borrower data validation passed")
    return True, ""

