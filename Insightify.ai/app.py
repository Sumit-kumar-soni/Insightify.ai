import streamlit as st
import os
from dotenv import load_dotenv
from modules import data_loader, cleaner, analyzer, visualizer, ai_insights
from utils.logger import setup_logger

# Initialize logger and environment variables
logger = setup_logger()
load_dotenv()

st.set_page_config(page_title="AutoData AI", layout="wide", initial_sidebar_state="expanded")

def main():
    st.sidebar.title("🤖 AutoData AI")
    st.sidebar.markdown("Upload, Clean, Analyze, and Extract Insights.")
    
    uploaded_file = st.sidebar.file_uploader("Upload Dataset", type=['csv', 'xlsx', 'json'])
    
    if uploaded_file:
        try:
            # 1. Load Data
            df, file_size_mb = data_loader.load_file(uploaded_file)
            st.sidebar.success(f"File loaded! Size: {file_size_mb:.2f} MB")
            
            # UI Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["🔍 Data & EDA", "🧹 Data Cleaning", "📊 Dashboard", "🤖 AI Insights"])
            
            with tab1:
                st.subheader("Data Preview")
                st.dataframe(df.head(100))
                
                st.subheader("Exploratory Data Analysis (EDA)")
                stats_df = analyzer.get_basic_stats(df)
                st.dataframe(stats_df)
                
            with tab2:
                st.subheader("Automated Cleaning")
                if st.button("Run Auto-Clean"):
                    with st.spinner("Cleaning data..."):
                        df_clean, cleaning_log = cleaner.auto_clean(df)
                        st.session_state['cleaned_df'] = df_clean
                        st.success("Cleaning Complete!")
                        for log_item in cleaning_log:
                            st.write(log_item)
                        
            with tab3:
                st.subheader("Interactive Dashboard")
                if 'cleaned_df' in st.session_state:
                    visualizer.generate_dashboard(st.session_state['cleaned_df'])
                else:
                    st.info("Please clean the data first in the Data Cleaning tab.")
                    
            with tab4:
                st.subheader("AI-Powered Insights")
                if 'cleaned_df' in st.session_state:
                    if st.button("Generate Insights"):
                        with st.spinner("Analyzing trends..."):
                            insights = ai_insights.generate_summary(st.session_state['cleaned_df'])
                            st.write(insights)
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            st.error(f"An error occurred while processing your file. Please check the format.")

if __name__ == "__main__":
    main()
