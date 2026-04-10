import pandas as pd
import os
import google.generativeai as genai

def generate_summary(df):
    # 1. Fetch the API key securely from .env
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Fallback if the key is missing
    if not api_key or api_key == "your_actual_api_key_goes_here":
        return "⚠️ **Error:** GEMINI_API_KEY not found. Please add your real key to the .env file."
        
    # 2. Configure the Gemini client
    genai.configure(api_key=api_key)
    
    # 3. Prepare the data summary
    stats = df.describe().to_string()
    data_types = df.dtypes.to_string()
    
    prompt = f"""
    Act as an expert Data Scientist. Analyze the following dataset summary and provide 3-5 key actionable business insights.
    
    Data Types:
    {data_types}
    
    Statistical Summary:
    {stats}
    
    Format your response in plain English using bullet points. Focus on what the numbers mean, not just repeating them.
    """
    
    try:
        # 4. Call the Gemini API
        # Using gemini-1.5-flash as it is highly efficient for fast text/data reasoning
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        
        return response.text
        
    except Exception as e:
        # Catch any API errors (like rate limits or invalid keys) so the app doesn't crash
        return f"❌ **An error occurred with the AI:** {str(e)}"
