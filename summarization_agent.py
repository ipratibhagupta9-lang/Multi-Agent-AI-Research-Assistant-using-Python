from groq import Groq 
from dotenv import load_dotenv
import os
print("✅ Groq summarization_agent.py loaded")
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_text(text):
    prompt = f"""
You are an expert AI Research Assistant.

Analyze the following research paper abstract and generate a structured summary.

Sections:
1. Research Objective
2. Methodology
3. Abstract Overview
4. Key Findings
5. Limitations
6. Future Scope
7. Conclusion

Abstract:
{text}
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional AI research paper summarizer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=900
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Summary generation failed.\n\nError: {e}"