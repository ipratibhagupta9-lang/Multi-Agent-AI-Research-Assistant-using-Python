from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_report(topic, summaries, analysis):

    prompt = f"""
You are a professional academic research report writer.

IMPORTANT PROJECT INFORMATION:
MAARA stands for:
"Multi-Agent AI Research Assistant"

Never use any other expansion of MAARA.

Research Topic:
{topic}

Retrieved Paper Summaries:
{summaries}

Research Gap Analysis:
{analysis}


IMPORTANT RULES:

1. Write the report strictly according to the provided Research Topic.

2. Use the retrieved papers and research gap analysis as the
   primary source of information.

3. Do NOT invent papers, authors, datasets, experiments,
   numerical results, citations, or references.

4. Do NOT change the meaning of the retrieved papers.

5. Do NOT introduce unrelated research topics.

6. If anti-collusion, value systems, conventions, reinforcement
   learning, or other concepts appear in the retrieved papers,
   discuss them only as part of the literature review and
   research-gap analysis. Do not automatically make them the
   main research topic.

7. MAARA must always mean:
   Multi-Agent AI Research Assistant.

8. The proposed MAARA system should be described as a research
   assistant that supports:
   - research paper retrieval
   - paper ranking
   - paper summarization
   - research gap identification
   - structured academic report generation

9. Do not claim that MAARA itself solves or experimentally proves
   the research gaps unless such evidence is explicitly provided.

10. Use formal academic English.

11. Avoid unnecessary repetition.

12. Write approximately 1500–2200 words.

13. Use clear academic headings and subheadings.


GENERATE THE REPORT IN THIS EXACT STRUCTURE:

# Research Report

## Research Topic

Clearly state the provided research topic.

## Abstract

Provide a concise academic summary of the research topic,
reviewed literature, identified research gaps, and the role
of the proposed MAARA system.

## 1. Introduction

Explain:
- background of the research topic
- importance of the research area
- motivation for reviewing existing research
- purpose of the report

## 2. Literature Review

Discuss the retrieved papers.

For each paper include:

### Paper 1
- Title
- Main research focus
- Method / approach
- Key findings
- Limitations or research gap

### Paper 2
- Title
- Main research focus
- Method / approach
- Key findings
- Limitations or research gap

Continue this format for all retrieved papers.

Do not invent information that is not available in the summaries.

## 3. Research Gap Analysis

### 3.1 Common Research Area

### 3.2 Common Techniques and Approaches

### 3.3 Common Limitations

### 3.4 Identified Research Gap

### 3.5 Future Research Directions

Clearly distinguish between gaps explicitly mentioned in the
papers and gaps inferred from the provided analysis.

## 4. Proposed MAARA System

Explain:

MAARA = Multi-Agent AI Research Assistant.

Describe how MAARA supports the research process through:
- Search Agent
- Paper Retrieval
- Paper Ranking
- Summarization Agent
- Critic / Research Gap Analysis
- Report Writer
- Final Research Report

Do not claim experimental performance unless evidence is provided.

## 5. System Workflow

Explain the workflow:

Research Topic
↓
Search Agent
↓
Paper Retrieval
↓
Paper Ranking
↓
Summarization
↓
Critic / Gap Analysis
↓
Report Writer
↓
Final Research Report

## 6. Limitations

Discuss limitations of the reviewed research and limitations
of the proposed MAARA research-assistant approach.

Do not invent experimental limitations.

## 7. Future Scope

Provide at least 5 realistic future research directions based
on the reviewed papers and identified research gaps.

## 8. Conclusion

Summarize the literature review, major research gaps, and the
role of MAARA.

## References

List only the retrieved papers that are actually provided in
the input.

Do not invent authors, publication venues, years, DOI numbers,
or URLs.


FINAL REQUIREMENT:

The final report must remain focused on the provided Research Topic.

Do not replace the research topic with a different topic.
Do not introduce unrelated concepts as the central theme.
"""


    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert academic research report writer. "
                        "Write accurate, formal, well-structured academic reports. "
                        "Use only the information provided by the user."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
            max_tokens=3500,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:

        return f"""
# Research Report Generation Failed

Error:
{e}
"""