import streamlit as st
from pathlib import Path
import logging
from ui.config.settings import PAGE_ICONS
from ui.styles import apply_global_styles, render_header
from ui.utils.model_loader import initialize_model
from ui.config.settings import get_model_path
from ui import pages

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def configure_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Loan Default Risk Predictor",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def render_sidebar():
    """Render sidebar navigation."""
    st.sidebar.markdown("### ⚙️ Navigation")
    selected_page = st.sidebar.radio(
        "Pages",
        ["Prediction", "Batch Analysis", "Model Info"],
        format_func=lambda x: f"{PAGE_ICONS.get(x.lower().replace(' ', '_'), '')} {x}",
    )
    return selected_page

def render_app(predictor):
    """Render main application UI."""
    render_header(
        "🏦 Loan Default Risk Prediction",
        "Advanced AI-Powered Risk Assessment System"
    )
    
    selected_page = render_sidebar()
    logger.info(f"Navigating to: {selected_page}")
    
    if selected_page == "Prediction":
        pages.prediction.render(predictor)
    elif selected_page == "Batch Analysis":
        pages.batch_analysis.render(predictor)
    else:
        pages.model_info.render(predictor)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; margin-top: 3rem;'>
        <p style='font-size: 0.9rem;'>
            🏦 Production-Grade Loan Default Risk Prediction System<br>
            Powered by Advanced Machine Learning
        </p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application entry point."""
    try:
        logger.info("Initializing application")
        configure_page()
        apply_global_styles()
        
        model_path = get_model_path()
        if not model_path:
            st.error("❌ Model file not found. Please ensure models are in the 'models/' directory.")
            logger.error("Model path not found")
            st.stop()
        
        logger.info(f"Loading model from: {model_path}")
        predictor = initialize_model(model_path)
        render_app(predictor)
        logger.info("Application rendered successfully")
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        st.error(f"❌ Application Error: {str(e)}")
        st.stop()

if __name__ == "__main__":
    main()

