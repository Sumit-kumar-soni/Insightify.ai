import pandas as pd
import os

def generate_summary(df):
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Create a statistical summary string to pass to the LLM
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
    
    # --- PROTOTYPE MOCK RESPONSE ---
    # Once you install the openai library, replace this return with the actual API call.
    if api_key == "your_openai_api_key_here" or not api_key:
         return """
         *(Mock Insights - Please add your OpenAI API Key to .env to enable real AI generation)*
         * **Outlier Detected:** The maximum value in your dataset is significantly higher than the 75th percentile, indicating potential anomalies or high-value targets.
         * **Data Skew:** Several numerical features show a strong right-skew, suggesting that a small percentage of rows account for the majority of the total value.
         * **Recommendation:** Group your categorical data by the highest performing numerical metric to identify your most valuable segments.
         """
    else:
        # Pseudo-code for real implementation:
        # client = OpenAI(api_key=api_key)
        # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
        # return response.choices[0].message.content
        pass
