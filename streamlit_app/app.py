"""
Node Authentication Trust System - Streamlit Web Application
Upload CSV file and get predictions with trust scores

Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import sys
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import custom modules
from utils.model_loader import ModelLoader
from utils.data_processor import DataProcessor
from utils.visualizer import Visualizer

# Page configuration
st.set_page_config(
    page_title="Node Authentication System",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .danger-box {
        background-color: #f8d7da;
        border: 2px solid #dc3545;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Main application function"""
    
    # Header
    st.markdown('<p class="main-header">🔐 Node Authentication Trust System</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/security-checked.png", width=100)
        st.title("Navigation")
        # page = st.radio("Go to", ["🏠 Home", "📤 Upload & Predict", "📊 Batch Analysis", "ℹ️ About"])
        page = st.radio("Go to", ["🏠 Home", "📤 Upload & Predict", "ℹ️ About"])
        
        st.markdown("---")
        st.markdown("### Model Info")
        st.info("""
        **Algorithm:** SVM (RBF Kernel)  
        **Accuracy:** 96.91%  
        **Precision:** 98.42%  
        **ROC-AUC:** 99.49%
        """)
    
    # Route to pages
    if page == "🏠 Home":
        show_home_page()
    elif page == "📤 Upload & Predict":
        show_upload_page()
    # elif page == "📊 Batch Analysis":
        # show_batch_analysis_page()
    elif page == "ℹ️ About":
        show_about_page()


def show_home_page():
    """Home page with welcome message and instructions"""
    st.title("Welcome to the Node Authentication System")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 Purpose")
        st.write("""
        This system uses Machine Learning to authenticate network nodes 
        and detect potential security threats in real-time.
        """)
    
    with col2:
        st.markdown("### 🚀 Features")
        st.write("""
        - CSV file upload for batch predictions
        - Individual node authentication
        - Trust score (0-100) calculation
        - Visual analytics and reports
        """)
    
    with col3:
        st.markdown("### 🔒 Security Levels")
        st.write("""
        - **High (66-100):** ✅ Allow Access
        - **Medium (33-66):** ⚠️ Monitor
        - **Low (0-33):** 🛑 Block Access
        """)
    
    st.markdown("---")
    
    # Quick stats
    st.subheader("📈 System Performance")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Accuracy", "96.91%", "+2.86%")
    col2.metric("Precision", "98.42%", "+1.08%")
    col3.metric("Recall", "94.34%", "-0.03%")
    col4.metric("F1-Score", "96.34%", "+1.42%")
    
    st.markdown("---")
    
    # Getting started
    st.subheader("🚀 Getting Started")
    st.write("1. Click on **'Upload & Predict'** in the sidebar")
    st.write("2. Upload a CSV file with network connection features")
    st.write("3. View predictions and trust scores")
    st.write("4. Download detailed reports")


def show_upload_page():
    """Upload page for CSV file prediction"""
    st.title("📤 Upload CSV & Get Predictions")
    
    # Initialize model loader
    try:
        with st.spinner("Loading models..."):
            model_loader = ModelLoader('../models')
            st.success("✅ Models loaded successfully!")
    except Exception as e:
        st.error(f"❌ Error loading models: {e}")
        st.stop()
    
    # File uploader
    st.markdown("### Upload Your CSV File")
    st.info("📋 Your CSV should contain 41 network connection features (or match the training data format)")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # Load data
            df = pd.read_csv(uploaded_file)
            
            st.success(f"✅ File uploaded successfully! ({len(df)} rows)")
            
            # Show preview
            with st.expander("👁️ View Data Preview", expanded=True):
                st.dataframe(df.head(10), use_container_width=True)
                st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
            
            # Process data
            st.markdown("---")
            st.markdown("### 🔄 Processing Data...")
            
            processor = DataProcessor(model_loader)
            
            # Validate and prepare data
            with st.spinner("Validating data..."):
                processed_df, issues = processor.validate_and_prepare(df)
            
            if issues:
                st.warning(f"⚠️ Found {len(issues)} issues:")
                for issue in issues[:5]:  # Show first 5 issues
                    st.write(f"- {issue}")
            
            # Make predictions
            if st.button("🎯 Generate Predictions", type="primary"):
                with st.spinner("Making predictions..."):
                    results_df = processor.predict(processed_df)
                
                st.success("✅ Predictions complete!")
                
                # Display results
                display_results(results_df)
                
                # Download button
                csv = results_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results CSV",
                    data=csv,
                    file_name=f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
        except Exception as e:
            st.error(f"❌ Error processing file: {e}")
            st.write("**Troubleshooting:**")
            st.write("- Ensure your CSV has the correct features")
            st.write("- Check for missing or invalid values")
            st.write("- Refer to the sample data format")


def display_results(results_df):
    """Display prediction results with visualizations"""
    st.markdown("---")
    st.markdown("### 📊 Prediction Results")
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    total = len(results_df)
    blocked = len(results_df[results_df['action'] == 'BLOCK'])
    monitored = len(results_df[results_df['action'] == 'MONITOR'])
    allowed = len(results_df[results_df['action'] == 'ALLOW'])
    
    col1.metric("Total Analyzed", total)
    col2.metric("🛑 Blocked", blocked, f"{blocked/total*100:.1f}%")
    col3.metric("⚠️ Monitor", monitored, f"{monitored/total*100:.1f}%")
    col4.metric("✅ Allowed", allowed, f"{allowed/total*100:.1f}%")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 Results Table", "📊 Visualizations", "🔍 Detailed Analysis"])
    
    with tab1:
        st.dataframe(results_df, use_container_width=True)
    
    with tab2:
        visualizer = Visualizer()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Action distribution pie chart
            fig = visualizer.create_action_distribution_chart(results_df)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Trust score distribution
            fig = visualizer.create_trust_score_distribution(results_df)
            st.plotly_chart(fig, use_container_width=True)
        
        # Trust score by prediction
        fig = visualizer.create_trust_score_by_prediction(results_df)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Show high-risk detections
        high_risk = results_df[results_df['action'] == 'BLOCK']
        if len(high_risk) > 0:
            st.markdown("#### 🚨 High Risk Detections (BLOCKED)")
            st.dataframe(high_risk[['prediction', 'trust_score', 'confidence', 'recommendation']], 
                        use_container_width=True)
        
        # Show medium risk
        medium_risk = results_df[results_df['action'] == 'MONITOR']
        if len(medium_risk) > 0:
            st.markdown("#### ⚠️ Medium Risk Detections (MONITOR)")
            st.dataframe(medium_risk[['prediction', 'trust_score', 'confidence', 'recommendation']].head(10), 
                        use_container_width=True)
        
        # Statistics
        st.markdown("#### 📈 Statistical Summary")
        st.dataframe(results_df[['trust_score', 'confidence']].describe())


def show_batch_analysis_page():
    """Batch analysis page for comparing multiple files"""
    st.title("📊 Batch Analysis & Comparison")
    st.info("Upload multiple CSV files to compare predictions and analyze trends")
    
    st.write("🚧 This feature is under development")
    st.write("Coming soon:")
    st.write("- Compare predictions across multiple datasets")
    st.write("- Trend analysis over time")
    st.write("- Export comprehensive reports")


def show_about_page():
    """About page with system information"""
    st.title("ℹ️ About This System")
    
    st.markdown("""
    ### 🔐 Node Authentication Trust System
    
    This system uses Machine Learning to authenticate network nodes and detect potential security threats.
    
    #### 🎯 Key Features:
    - **ML Algorithm:** Support Vector Machine (SVM) with RBF Kernel
    - **Trust Scoring:** 0-100 scale for risk assessment
    - **Real-time Processing:** Fast predictions (~7000/second)
    - **High Accuracy:** 96.91% classification accuracy
    
    #### 📊 Model Performance:
    - **Accuracy:** 96.91%
    - **Precision:** 98.42% (low false alarms)
    - **Recall:** 94.34% (catches most threats)
    - **F1-Score:** 96.34%
    - **ROC-AUC:** 99.49% (excellent discrimination)
    
    #### 🛡️ Security Levels:
    1. **High Trust (66-100):** ✅ ALLOW - Grant access, low risk
    2. **Medium Trust (33-66):** ⚠️ MONITOR - Additional verification needed
    3. **Low Trust (0-33):** 🛑 BLOCK - Deny access, high risk
    
    #### 📋 Required Features (41 total):
    Your CSV should include network connection features such as:
    - Duration, protocol type, service, flag
    - Source and destination bytes
    - Login status, connection counts
    - Error rates, service rates
    - And 32 more features...
    
    #### 🔧 Technical Stack:
    - **ML Framework:** scikit-learn
    - **Web Framework:** Streamlit
    - **Visualization:** Plotly
    - **Data Processing:** Pandas, NumPy
    
    #### 📞 Support:
    For questions or issues, refer to the project documentation.
    
    ---
    **Version:** 1.0.0  
    **Last Updated:** October 2025
    """)


if __name__ == "__main__":
    main()
