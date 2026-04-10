import streamlit as st
import plotly.express as px

def generate_dashboard(df):
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Feature Distribution")
        if num_cols:
            hist_col = st.selectbox("Select numerical column", num_cols, key="hist")
            fig1 = px.histogram(df, x=hist_col, marginal="box", template="plotly_white")
            st.plotly_chart(fig1, use_container_width=True)
            
    with col2:
        st.write("### Categorical Breakdown")
        if cat_cols:
            pie_col = st.selectbox("Select categorical column", cat_cols, key="pie")
            # Limit pie charts to top 10 categories to avoid visual clutter
            top_cats = df[pie_col].value_counts().nlargest(10).reset_index()
            top_cats.columns = [pie_col, 'count']
            fig2 = px.pie(top_cats, names=pie_col, values='count', hole=0.4, template="plotly_white")
            st.plotly_chart(fig2, use_container_width=True)
            
    st.write("### Correlation Heatmap")
    if len(num_cols) > 1:
        corr_matrix = df[num_cols].corr()
        fig3 = px.imshow(corr_matrix, text_auto=".2f", color_continuous_scale='Blues')
        st.plotly_chart(fig3, use_container_width=True)
