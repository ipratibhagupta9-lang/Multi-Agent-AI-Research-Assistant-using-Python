MAARA - MULTI-AGENT AI RESEARCH ASSISTANT

PROJECT OVERVIEW

MAARA (Multi-Agent AI Research Assistant) is a Python-based research
assistant developed as part of an Artificial Intelligence internship at
Vishwakarma University - VU Pune.

The project helps users explore research papers, understand their
abstracts, identify possible research gaps, and prepare structured
research reports. It uses multiple agents, with each agent responsible
for a specific stage of the research workflow.

KEY FEATURES

-   Search research papers stored in a local ChromaDB collection.
-   Generate concise summaries of research-paper abstracts.
-   Analyze papers to identify possible research gaps and future
    directions.
-   Generate structured research reports.
-   View paper similarity scores and publication-year distribution.
-   Select papers and export generated reports as TXT, PDF, or DOCX
    files.
-   Use a Streamlit dashboard to interact with the system.

HOW IT WORKS

1.  Search Agent: Searches the pre-built local research-paper collection
    for papers relevant to the user’s query.

2.  Summarization Agent: Produces a concise summary of the selected
    paper abstracts.

3.  Critic Agent: Reviews the available research information and
    highlights possible research gaps.

4.  Report Writer Agent: Combines the generated information into a
    structured research report.

TECHNOLOGIES USED

-   Python
-   Streamlit
-   ChromaDB
-   Sentence Transformers (all-MiniLM-L6-v2)
-   Groq API
-   arXiv API for dataset preparation
-   Matplotlib
-   ReportLab
-   python-docx

PROJECT STRUCTURE

A representative project structure is shown below. Your actual folder
and file names may differ.

MAARA/ |– app.py |– search_agent.py |– summarization_agent.py |–
critic_agent.py |– report_writer.py |– data/ | |– papers.csv |–
chroma_db/ |– requirements.txt |– .env |– .gitignore |– README.md

GETTING STARTED

Requirements: - Python installed on your computer - Git (if you want to
clone the repository) - A Groq API key, if required by your code

1.  Clone your repository:

    git clone https:https://github.com/ipratibhagupta9-lang/Multi-Agent-AI-Research-Assistant-using-Python

2.  Create a virtual environment:

    python -m venv venv

3.  Activate the environment on Windows:

    venv

    On macOS or Linux:

    source venv/bin/activate

4.  Install the required packages:

    pip install -r requirements.txt

5.  Create a file named .env in the project folder and add your API key:

    GROQ_API_KEY=your_groq_api_key_here

    Check your source code for the exact environment-variable name it
    expects. Never upload a real API key or password to GitHub.

6.  Run the Streamlit application:

    streamlit run app.py

IMPORTANT NOTES

-   MAARA searches a pre-built local research-paper collection at query
    time; it does not perform live internet or arXiv searches for every
    user query.
-   The paper collection and database must be prepared and available for
    the application to work as expected.
-   Confirm the actual filenames, folder structure, API variable name,
    and setup commands against your code before publishing this README.
-   Do not upload your .env file, API keys, passwords, or other private
    credentials to GitHub.

FUTURE IMPROVEMENTS

-   Add live research-paper retrieval.
-   Improve citation and reference generation.
-   Add more evaluation options for summaries and research-gap
    suggestions.
-   Improve error handling and documentation.
-   Expand the supported research sources.

WHAT I LEARNED

Building MAARA provided practical experience with Python, semantic
search, vector databases, language-model APIs, multi-agent workflows,
and report generation. It also helped me understand how separate
components can work together to support a research task.

AUTHOR

Pratibha Gupta 
