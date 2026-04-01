import streamlit as st
import logging

logger = logging.getLogger(__name__)

def safe_predict(predictor, features: dict) -> dict | None:
    """
    Safely execute prediction with comprehensive error handling.
    
    Args:
        predictor: LoanDefaultPredictor instance
        features: Dictionary of borrower features
        
    Returns:
        Prediction result dictionary or None if error occurs
    """
    try:
        # Validate features exist
        if not features or len(features) == 0:
            st.error("❌ **Error:** No borrower data provided. Please fill in all fields.")
            return None
        
        # Validate required feature count
        from src.predict import LoanDefaultPredictor
        required_count = len(LoanDefaultPredictor.REQUIRED_FEATURES)
        if len(features) < required_count:
            st.error(f"❌ **Error:** Missing required features. Expected {required_count}, got {len(features)}")
            return None
        
        logger.info(f"Executing prediction with {len(features)} features")
        result = predictor.predict_single(features)
        
        if result is None:
            st.error("❌ **Error:** Prediction returned no result. Please try again.")
            return None
        
        # Validate result structure
        if 'probability_default' not in result or 'probability_no_default' not in result:
            st.error("❌ **Error:** Invalid prediction result structure.")
            return None
        
        logger.info(f"Prediction successful: Default prob = {result['probability_default']:.2%}")
        return result
    
    except ValueError as e:
        error_msg = str(e)
        logger.error(f"Validation error: {error_msg}")
        st.error(f"❌ **Validation Error:**\\n{error_msg}")
        return None
    
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Prediction failed: {error_msg}")
        st.error(f"❌ **Prediction Error:**\\n{error_msg}\\n\\n**Tip:** Ensure all form fields are properly filled.")
        return None

def format_currency(value: int | float) -> str:
    """Format numeric value as currency with proper handling."""
    if value is None or (isinstance(value, float) and value != value):  # NaN check
        return "$0.00"
    try:
        return f"${value:,.2f}"
    except:
        return "$0.00"

def format_percentage(value: float) -> str:
    """Format float as percentage with 1 decimal place and 100% cap."""
    if value is None or (isinstance(value, float) and value != value):  # NaN check
        return "0.0%"
    try:
        # Cap at 100% for display
        capped_value = min(float(value), 1.0)
        return f"{capped_value:.1%}"
    except:
        return "0.0%"

def format_decimal(value: float, places: int = 2) -> str:
    """Format float with specified decimal places and error handling."""
    if value is None or (isinstance(value, float) and value != value):  # NaN check
        return "0." + "0" * places
    try:
        return f"{float(value):.{places}f}"
    except:
        return "0." + "0" * places

def format_count(value: int) -> str:
    """Format integer with comma separators and error handling."""
    if value is None or not isinstance(value, (int, float)):
        return "0"
    try:
        return f"{int(value):,}"
    except:
        return "0"

def format_probability_confidence(prob: float) -> str:
    """Format probability with confidence level label."""
    if prob is None or (isinstance(prob, float) and prob != prob):
        return "Unknown (0%)"
    
    try:
        p = float(prob)
        if p >= 0.8:
            return f"Very High ({p:.1%})"
        elif p >= 0.6:
            return f"High ({p:.1%})"
        elif p >= 0.4:
            return f"Medium ({p:.1%})"
        elif p >= 0.2:
            return f"Low ({p:.1%})"
        else:
            return f"Very Low ({p:.1%})"
    except:
        return "Unknown"

