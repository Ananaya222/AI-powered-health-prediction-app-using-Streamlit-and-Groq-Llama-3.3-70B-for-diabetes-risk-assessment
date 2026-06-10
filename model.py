import os
import re
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_groq_client():
    """Initialize Groq client using API key from environment variables."""
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        st.warning("⚠️ Groq API key not found. Using rule‑based fallback.")
        return None
    
    return Groq(api_key=api_key)

def rule_based_fallback(glucose, haemoglobin, cholesterol):
    """Fallback logic when Groq API is unavailable."""
    if glucose > 125 or haemoglobin > 15.5 or cholesterol > 240:
        return "⚠️ **High diabetes risk** – multiple values exceed healthy ranges. Please consult a doctor.\n\n*(Using fallback logic – API key missing)*"
    else:
        return "✅ **Low diabetes risk** – your values are within healthy ranges. Maintain a healthy lifestyle.\n\n*(Using fallback logic – API key missing)*"

def predict_risk(glucose, haemoglobin, cholesterol, age=30):
    """Call Groq API to generate a personalized health risk assessment."""
    client = get_groq_client()
    
    if not client:
        return rule_based_fallback(glucose, haemoglobin, cholesterol)
    
    try:
        prompt = f"""You are a medical AI assistant. Analyze these health metrics:

- Glucose: {glucose} mg/dL (normal range: 70-99 fasting)
- Haemoglobin: {haemoglobin} g/dL (normal range: 13.5-17.5 for men, 12.0-15.5 for women)
- Cholesterol: {cholesterol} mg/dL (normal range: <200)
- Age: {age} years

Provide a short, professional assessment of diabetes/metabolic risk. Output exactly in this format:

Risk Level: [either "High" or "Low"]
Probability: [X]%
Explanation: [1-2 sentences]

Keep the tone reassuring but factual. Do not add extra text."""

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a precise medical assistant. Return only the requested format."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=200
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Parse the response
        risk_level = "Low"
        probability = 20
        explanation = "Unable to parse AI response."
        
        for line in result_text.split('\n'):
            if "Risk Level:" in line:
                risk_level = "High" if "High" in line else "Low"
            elif "Probability:" in line:
                import re
                prob_str = re.search(r'(\d+)', line)
                if prob_str:
                    probability = int(prob_str.group(1))
            elif "Explanation:" in line:
                explanation = line.replace("Explanation:", "").strip()
        
        probability = max(0, min(100, probability))
        
        if risk_level == "High":
            final = f"⚠️ **High diabetes risk** (probability: {probability}%)\n\n{explanation}\n\n*(Powered by Groq Llama 3.3 70B)*"
        else:
            final = f"✅ **Low diabetes risk** (probability: {probability}%)\n\n{explanation}\n\n*(Powered by Groq Llama 3.3 70B)*"
        
        return final
        
    except Exception as e:
        st.error(f"Groq API error: {str(e)}")
        return rule_based_fallback(glucose, haemoglobin, cholesterol)
