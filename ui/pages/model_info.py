import streamlit as st
import pandas as pd
from datetime import datetime
from ui.config.settings import DATASET_INFO, RISK_LEVELS
from ui.components.metrics import render_feature_table, render_risk_guidelines

def render(predictor):
    st.markdown("### ℹ️ System Information")
    
    col_info1, col_info2 = st.columns(2, gap="large")
    
    with col_info1:
        st.markdown("#### 🤖 Model Details")
        st.markdown(f"""
        **Model Name:** {predictor.model_name}
        
        **Type:** Binary Classification
        
        **Task:** Default Risk Prediction
        
        **Output:** Probability & Classification
        """)
    
    with col_info2:
        st.markdown("#### 📊 Dataset Information")
        st.markdown(f"""
        **Total Records:** {DATASET_INFO['total_records']:,}
        
        **Train-Test Split:** {DATASET_INFO['train_split']:.0%} / {1-DATASET_INFO['train_split']:.0%}
        
        **Feature Count:** {DATASET_INFO['features']}
        
        **Target Variable:** {DATASET_INFO['target']}
        """)
    
    st.markdown("---")
    st.markdown("#### 📝 Feature Descriptions")
    render_feature_table()
    
    st.markdown("---")
    st.markdown("#### 🎯 Risk Assessment Guidelines")
    render_risk_guidelines()
    
    st.markdown("---")
    st.markdown("#### 📌 Key Points")
    st.markdown("""
    - **Data Preprocessing:** Categorical encoding, feature scaling applied
    - **Class Imbalance:** Handled using SMOTE oversampling
    - **Model Training:** Hyperparameter tuning via GridSearchCV
    - **Validation:** Cross-validation and stratified train-test split
    - **Performance:** Optimized for precision and recall balance
    """)
    
    st.markdown("---")
    st.markdown(f"**Last Updated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
