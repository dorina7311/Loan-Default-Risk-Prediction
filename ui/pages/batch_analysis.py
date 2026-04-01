import streamlit as st
import pandas as pd
from pathlib import Path
from ui.components.charts import create_risk_distribution_pie
from ui.styles import render_warning_box, render_info_box
from ui.utils.preprocessor import encode_batch_data, validate_batch_columns
import logging

logger = logging.getLogger(__name__)

def render(predictor):
    st.markdown("### 📈 Batch Prediction Analysis")
    st.markdown("Process multiple borrower records for comprehensive risk assessment")
    
    # Initialize session state for batch uploads
    if 'batch_results' not in st.session_state:
        st.session_state.batch_results = None
    if 'batch_data' not in st.session_state:
        st.session_state.batch_data = None
    
    tab_upload, tab_sample = st.tabs(["📤 Upload CSV", "📊 Sample Dataset"])
    
    with tab_upload:
        st.markdown("**📋 Expected CSV Format:**")
        st.markdown("""
        Required columns: Age, Income, LoanAmount, CreditScore, MonthsEmployed, NumCreditLines, 
        InterestRate, LoanTerm, DTIRatio, Education, EmploymentType, MaritalStatus, 
        HasMortgage, HasDependents, LoanPurpose, HasCoSigner
        """)
        
        uploaded_file = st.file_uploader("Choose CSV file", type="csv", key="batch_upload")
        
        if uploaded_file is not None:
            try:
                with st.spinner('📂 Loading CSV file...'):
                    df = pd.read_csv(uploaded_file)
                    st.session_state.batch_data = df
                
                st.success(f"✅ Dataset loaded: **{df.shape[0]} rows** × **{df.shape[1]} columns**")
                st.info(f"Columns found: {', '.join(df.columns.tolist())}")
                
                # Show data preview
                with st.expander("📊 Preview data", expanded=False):
                    st.dataframe(df.head(10), use_container_width=True, height=300)
                
                is_valid, message = validate_batch_columns(df)
                if not is_valid:
                    st.error(f"❌ Validation Error:\\n{message}")
                else:
                    st.success("✅ CSV format validated successfully")
                    
                    if st.button("🔍 Predict All Records", use_container_width=True, key="predict_upload", type="primary"):
                        try:
                            with st.spinner('⚙️ Preprocessing data...'):
                                df_encoded = encode_batch_data(df)
                                logger.info(f"Encoded data shape: {df_encoded.shape}")
                            
                            with st.spinner('🤖 Running predictions...'):
                                results = predictor.predict_batch(df_encoded)
                                st.session_state.batch_results = results
                            
                            st.success("✅ Predictions completed successfully!")
                            
                            # Display results with proper formatting
                            st.markdown("---")
                            st.markdown("### 📋 Prediction Results")
                            
                            # Use expandable container for results
                            with st.expander("📊 View all results (click to expand)", expanded=True):
                                # Format probabilities for display
                                display_results = results.copy()
                                if 'probability_default' in display_results.columns:
                                    display_results['probability_default'] = display_results['probability_default'].apply(lambda x: f"{x:.2%}")
                                if 'probability_no_default' in display_results.columns:
                                    display_results['probability_no_default'] = display_results['probability_no_default'].apply(lambda x: f"{x:.2%}")
                                
                                # Limit rows to prevent Pandas Styler max_elements error
                                max_rows = 1000
                                if len(display_results) > max_rows:
                                    st.warning(f"⚠️ Showing first {max_rows} of {len(display_results)} records. Use download button for full dataset.")
                                    display_results = display_results.head(max_rows)
                                
                                st.dataframe(
                                    display_results,
                                    use_container_width=True,
                                    height=400
                                )
                            
                            st.markdown("---")
                            st.markdown("### 📊 Summary Statistics")
                            
                            col_stat1, col_stat2, col_stat3 = st.columns(3, gap="large")
                            
                            default_count = (results['prediction'] == 1).sum()
                            default_pct = (default_count / len(results) * 100) if len(results) > 0 else 0
                            good_count = len(results) - default_count
                            
                            with col_stat1:
                                st.metric(
                                    "📊 Total Records",
                                    f"{len(results):,}",
                                    delta=None,
                                    delta_color="off"
                                )
                            with col_stat2:
                                st.metric(
                                    "⚠️ Default Risk Count",
                                    f"{default_count:,}",
                                    delta=f"{default_pct:.1f}%",
                                    delta_color="inverse"
                                )
                            with col_stat3:
                                st.metric(
                                    "✅ Good Risk Count",
                                    f"{good_count:,}",
                                    delta=f"{100-default_pct:.1f}%",
                                    delta_color="off"
                                )
                            
                            with st.spinner('📈 Generating risk distribution chart...'):
                                fig_pie = create_risk_distribution_pie(good_count, default_count)
                                st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
                            
                            st.markdown("---")
                            
                            # Download button
                            csv_export = results.to_csv(index=False)
                            st.download_button(
                                label="📥 Download Results as CSV",
                                data=csv_export,
                                file_name="prediction_results.csv",
                                mime="text/csv",
                                use_container_width=True,
                                type="primary"
                            )
                        
                        except Exception as e:
                            logger.error(f"Prediction error: {str(e)}")
                            st.error(f"❌ **Prediction Error:**\\n{str(e)}\\n\\n**Solution:** Verify CSV columns match expected format.")
            
            except pd.errors.ParserError as e:
                st.error(f"❌ **CSV Parsing Error:**\\n{str(e)}\\n\\nEnsure your CSV is properly formatted.")
            except Exception as e:
                logger.error(f"File processing error: {str(e)}")
                st.error(f"❌ **File Processing Error:**\\n{str(e)}")
    
    with tab_sample:
        st.markdown("Use the sample cleaned dataset for testing")
        
        data_path = Path(__file__).parent.parent.parent / "data" / "processed" / "cleaned_data.csv"
        
        if data_path.exists():
            if st.button("📊 Load Sample & Predict", use_container_width=True, key="predict_sample", type="primary"):
                try:
                    with st.spinner('📂 Loading sample data...'):
                        df = pd.read_csv(data_path)
                        sample_df = df.head(100)
                        st.success(f"✅ Sample loaded: **{sample_df.shape[0]} records**")
                    
                    with st.spinner('⚙️ Preprocessing sample data...'):
                        df_encoded = encode_batch_data(sample_df)
                        logger.info(f"Sample encoded shape: {df_encoded.shape}")
                    
                    with st.spinner('🤖 Running batch predictions...'):
                        results = predictor.predict_batch(df_encoded)
                        st.session_state.batch_results = results
                    
                    st.success("✅ Sample predictions completed!")
                    
                    # Display results
                    st.markdown("---")
                    st.markdown("### 📋 Sample Prediction Results")
                    
                    with st.expander("📊 View all results (click to expand)", expanded=True):
                        # Format probabilities for display
                        display_results = results.copy()
                        if 'probability_default' in display_results.columns:
                            display_results['probability_default'] = display_results['probability_default'].apply(lambda x: f"{x:.2%}")
                        if 'probability_no_default' in display_results.columns:
                            display_results['probability_no_default'] = display_results['probability_no_default'].apply(lambda x: f"{x:.2%}")
                        
                        st.dataframe(
                            display_results,
                            use_container_width=True,
                            height=400
                        )
                    
                    st.markdown("---")
                    st.markdown("### 📊 Sample Results Summary")
                    
                    col_stat1, col_stat2, col_stat3 = st.columns(3, gap="large")
                    
                    default_count = (results['prediction'] == 1).sum()
                    default_pct = (default_count / len(results) * 100) if len(results) > 0 else 0
                    good_count = len(results) - default_count
                    
                    with col_stat1:
                        st.metric("📊 Total Records", f"{len(results):,}")
                    with col_stat2:
                        st.metric("⚠️ Default Risk", f"{default_count:,} ({default_pct:.1f}%)")
                    with col_stat3:
                        st.metric("✅ Good Risk", f"{good_count:,} ({100-default_pct:.1f}%)")
                    
                    with st.spinner('📈 Generating chart...'):
                        fig_pie = create_risk_distribution_pie(good_count, default_count)
                        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
                    
                except Exception as e:
                    logger.error(f"Sample processing error: {str(e)}")
                    st.error(f"❌ **Processing Error:**\\n{str(e)}")
        else:
            render_warning_box("⚠️ Sample data not available. Please upload your own CSV file.")
