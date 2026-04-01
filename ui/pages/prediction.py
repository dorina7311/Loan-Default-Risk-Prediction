import streamlit as st
import pandas as pd
from ui.components.forms import build_borrower_form
from ui.components.charts import (
    create_default_gauge, create_probability_stacked_bar
)
from ui.components.metrics import render_result_metrics, render_borrower_summary
from ui.styles import render_info_box, render_risk_badge
from ui.utils.risk_assessment import get_risk_assessment, get_risk_recommendation
from ui.utils.formatters import safe_predict

def render(predictor):
    # Initialize session state for form submission
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
    if 'last_prediction' not in st.session_state:
        st.session_state.last_prediction = None
    if 'last_borrower_data' not in st.session_state:
        st.session_state.last_borrower_data = None
    
    col_form, col_results = st.columns([1, 1], gap="large")
    
    with col_form:
        st.markdown("### 📝 Borrower Information")
        st.markdown("Enter borrower details for comprehensive risk assessment")
        
        try:
            borrower_data, submitted = build_borrower_form()
        except Exception as e:
            st.error(f"Form Error: {str(e)}")
            submitted = False
            borrower_data = None
    
    with col_results:
        st.markdown("### 📊 Assessment Results")
        
        if submitted and borrower_data:
            # Mark as submitted and trigger prediction
            st.session_state.form_submitted = True
            st.session_state.last_borrower_data = borrower_data
            
            with st.spinner('⏳ Validating borrower data...'):
                import time
                time.sleep(0.3)
            
            with st.spinner('🔄 Analyzing borrower profile...'):
                result = safe_predict(predictor, borrower_data)
            
            if result is None:
                st.error("❌ Prediction failed. Please check your input values.")
                result = {}
            
            if result:
                st.session_state.last_prediction = result
                prob_default = result['probability_default']
                prob_no_default = result['probability_no_default']
                
                assessment = get_risk_assessment(prob_default)
                recommendation = get_risk_recommendation(assessment)
                
                render_risk_badge(assessment['level'], prob_default)
                
                with st.spinner('📊 Generating charts...'):
                    fig_gauge = create_default_gauge(prob_default)
                    st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False, 'responsive': True})
                    
                    render_result_metrics(prob_default, prob_no_default, predictor.model_name)
                    
                    fig_bar = create_probability_stacked_bar(prob_default, prob_no_default)
                    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False, 'responsive': True})
                
                st.markdown("---")
                st.markdown("### 💼 Recommendation & Risk Analysis")
                
                if prob_default > 0.7:
                    st.error(f"🔴 **HIGH RISK - {recommendation}**")
                    st.markdown("""\n**What this means:**
- The model predicts a **70%+ chance** this borrower will default
- Multiple risk factors indicate financial instability
- **Loan Status:** ❌ RECOMMEND DECLINE
""")
                elif prob_default > 0.5:
                    st.warning(f"🟠 **MEDIUM-HIGH RISK - {recommendation}**")
                    st.markdown(f"""\n**What this means:**
- Default probability is **{prob_default:.1%}** (above 50% threshold)
- Several concerning risk factors identified
- **Loan Status:** ⚠️ REQUEST ADDITIONAL DOCUMENTATION & GUARANTOR
""")
                elif prob_default > 0.3:
                    st.info(f"🟡 **MEDIUM RISK - {recommendation}**")
                    st.markdown(f"""\n**What this means:**
- Default probability is **{prob_default:.1%}** (slightly elevated)
- Some risk factors present but manageable
- **Loan Status:** ℹ️ PROCEED WITH CAUTION - MONITOR CLOSELY
""")
                else:
                    st.success(f"🟢 **LOW RISK - {recommendation}**")
                    st.markdown(f"""\n**What this means:**
- Default probability is only **{prob_default:.1%}** (very low risk)
- Strong financial profile with positive indicators
- **Loan Status:** ✅ RECOMMEND APPROVAL
""")
                
                st.markdown("---")
                st.markdown("### 📋 Borrower Profile Summary")
                render_borrower_summary(borrower_data)
        
        elif st.session_state.form_submitted and st.session_state.last_prediction:
            # Show cached result if form was previously submitted
            result = st.session_state.last_prediction
            borrower_data = st.session_state.last_borrower_data
            
            prob_default = result['probability_default']
            prob_no_default = result['probability_no_default']
            
            assessment = get_risk_assessment(prob_default)
            recommendation = get_risk_recommendation(assessment)
            
            render_risk_badge(assessment['level'], prob_default)
            
            fig_gauge = create_default_gauge(prob_default)
            st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False, 'responsive': True})
            
            render_result_metrics(prob_default, prob_no_default, predictor.model_name)
            
            fig_bar = create_probability_stacked_bar(prob_default, prob_no_default)
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False, 'responsive': True})
            
            st.markdown("---")
            st.markdown("### 💼 Recommendation & Risk Analysis")
            
            if prob_default > 0.7:
                st.error(f"🔴 **HIGH RISK - {recommendation}**")
                st.markdown("""\n**What this means:**
- The model predicts a **70%+ chance** this borrower will default
- Multiple risk factors indicate financial instability
- **Loan Status:** ❌ RECOMMEND DECLINE
""")
            elif prob_default > 0.5:
                st.warning(f"🟠 **MEDIUM-HIGH RISK - {recommendation}**")
                st.markdown(f"""\n**What this means:**
- Default probability is **{prob_default:.1%}** (above 50% threshold)
- Several concerning risk factors identified
- **Loan Status:** ⚠️ REQUEST ADDITIONAL DOCUMENTATION & GUARANTOR
""")
            elif prob_default > 0.3:
                st.info(f"🟡 **MEDIUM RISK - {recommendation}**")
                st.markdown(f"""\n**What this means:**
- Default probability is **{prob_default:.1%}** (slightly elevated)
- Some risk factors present but manageable
- **Loan Status:** ℹ️ PROCEED WITH CAUTION - MONITOR CLOSELY
""")
            else:
                st.success(f"🟢 **LOW RISK - {recommendation}**")
                st.markdown(f"""\n**What this means:**
- Default probability is only **{prob_default:.1%}** (very low risk)
- Strong financial profile with positive indicators
- **Loan Status:** ✅ RECOMMEND APPROVAL
""")
            
            st.markdown("---")
            st.markdown("### 📋 Borrower Profile Summary")
            render_borrower_summary(borrower_data)
        
        else:
            render_info_box("👆 Complete the form and click 'Predict Risk' to begin assessment")
    
    st.markdown("---")
    st.markdown("### 🧪 Test Scenarios")
    
    test_col1, test_col2, test_col3 = st.columns(3, gap="medium")
    
    with test_col1:
        if st.button("✅ Low Risk Profile", use_container_width=True):
            st.session_state.test_profile = "low_risk"
            st.rerun()
    
    with test_col2:
        if st.button("⚠️ Medium Risk Profile", use_container_width=True):
            st.session_state.test_profile = "medium_risk"
            st.rerun()
    
    with test_col3:
        if st.button("❌ High Risk Profile", use_container_width=True):
            st.session_state.test_profile = "high_risk"
            st.rerun()
