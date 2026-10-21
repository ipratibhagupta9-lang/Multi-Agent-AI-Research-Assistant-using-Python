from groq import Groq 
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def analyze_papers(summaries):

    prompt = f"""
You are an expert AI Research Critic.

Analyze the following summaries of research papers.

Generate a professional Research Gap Analysis.

Your response should include:

# 📊 Research Gap Analysis

## 🌍 Common Research Area

## ⚙️ Common Techniques

## ⚠️ Common Limitations

## 🔍 Identified Research Gap

## 🚀 Future Research Directions

## 📌 Overall Observation

Research Paper Summaries:

{summaries}
"""

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert AI Research Critic."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1000
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Research Gap Analysis Failed.\n\nError: {e}"