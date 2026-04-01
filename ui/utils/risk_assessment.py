import logging
from ui.config.settings import RISK_LEVELS

logger = logging.getLogger(__name__)

def get_risk_assessment(probability_default: float) -> dict:
    """
    Determine risk level based on default probability.
    
    Args:
        probability_default: Predicted probability of default (0-1)
        
    Returns:
        Dictionary with risk level, icon, color, action, and probability
    """
    for level_name, level_config in RISK_LEVELS.items():
        min_range, max_range = level_config['range']
        if min_range <= probability_default < max_range:
            logger.info(f"Risk assessment: {level_name} (probability: {probability_default:.2%})")
            return {
                'level': level_name,
                'icon': level_config['icon'],
                'color': level_config['color'],
                'action': level_config['action'],
                'probability': probability_default,
            }
    
    logger.warning(f"Probability out of range: {probability_default}")
    return {
        'level': 'VERY_HIGH',
        'icon': RISK_LEVELS['VERY_HIGH']['icon'],
        'color': RISK_LEVELS['VERY_HIGH']['color'],
        'action': RISK_LEVELS['VERY_HIGH']['action'],
        'probability': probability_default,
    }

def format_risk_display(assessment: dict) -> str:
    """
    Format risk assessment for display.
    
    Args:
        assessment: Risk assessment dictionary
        
    Returns:
        Formatted display string
    """
    return f"{assessment['icon']} {assessment['level'].replace('_', ' ')} RISK"

def get_risk_recommendation(assessment: dict) -> str:
    """
    Get the recommended action for the risk assessment.
    
    Args:
        assessment: Risk assessment dictionary
        
    Returns:
        Recommendation string
    """
    return assessment['action']

