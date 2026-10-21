# app.py
import streamlit as st
import time
from search_agent import search_papers
from summarization_agent import summarize_text
from critic_agent import analyze_papers
from report_writer import generate_report
#from pdf_generator import create_pdf
from maara_pdf import create_pdf
#from docx_generator import create_docx
from maara_docx import create_docx
import matplotlib.pyplot as plt

st.set_page_config(page_title="MAARA", page_icon="🤖", layout="wide")

defaults = {
    "papers": [],
    "searched": False,
    "topic": "",
    "summaries": {},
    "analysis": "",
    "report": "",
}
for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k]=v

st.sidebar.title("🤖 MAARA")
st.sidebar.markdown("---")

st.sidebar.subheader("📂 Navigation")

st.sidebar.write("🏠 Dashboard")
st.sidebar.write("🔍 Search Papers")
st.sidebar.write("📄 AI Summary")
st.sidebar.write("📊 Research Gap")
st.sidebar.write("📑 Final Report")
st.sidebar.write("⬇ Download Report")

st.sidebar.markdown("---")

st.sidebar.success("🟢 System Ready")

st.sidebar.markdown("**Version:** 1.0")

st.title("🤖 MAARA")
st.subheader("Multi-Agent AI Research Assistant")

topic = st.text_input("Enter Research Topic", value=st.session_state.topic)
search = st.button("🔍 Search Papers")

st.markdown("---")

c1,c2,c3,c4 = st.columns(4)
c1.metric("📄 Papers", len(st.session_state.papers))
c2.metric("🤖 Agents","4")
c3.metric("📊 Status","Completed" if st.session_state.searched else "Waiting")
c4.metric("📑 Report","Ready" if st.session_state.report else "Not Generated")

if search:
    if not topic.strip():
        st.warning("⚠ Please enter a research topic.")
        st.stop()
    with st.spinner("Searching research papers..."):
        p=st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            p.progress(i+1)
    st.session_state.papers=search_papers(topic)
    st.session_state.topic=topic
    st.session_state.searched=True
    st.session_state.summaries={}
    st.session_state.analysis=""
    st.session_state.report=""

if st.session_state.searched:
    st.success(f"✅ Search Completed for: {st.session_state.topic}")
    st.subheader("📚 Search Results")

    for i,paper in enumerate(st.session_state.papers,1):
        with st.expander(f"📄 Paper {i} - {paper['title']}"):
            st.write(f"**📅 Year:** {paper['year']}")
            st.write(f"**🎯 Similarity Score:** {paper['score']}")
            st.write("**📝 Abstract:**")
            st.write(paper["abstract"])
            selected = st.checkbox("📌 Select this paper for Research Gap Analysis", key=f"select_{i}")

            pid=f"paper_{i}"
            if st.button("🤖 Generate AI Summary", key=f"sum_{i}"):
                with st.spinner("Generating summary..."):
                    st.session_state.summaries[pid]=summarize_text(paper["abstract"])

            if pid in st.session_state.summaries:
                st.success("✅ Summary Ready")
                st.markdown(st.session_state.summaries[pid], unsafe_allow_html=True)
                
                
    
st.markdown("---")
st.subheader("📊 Dashboard Analytics")

if st.session_state.papers:

    # ==========================
    # Publication Year Chart
    # ==========================
    years = sorted([str(paper["year"]) for paper in st.session_state.papers])

    year_count = {}

    for year in years:
        year_count[year] = year_count.get(year, 0) + 1

    fig, ax = plt.subplots(figsize=(3,2))

    ax.bar(year_count.keys(), year_count.values())

    ax.set_title("Publication Year Distribution")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Papers")

    st.pyplot(fig)


    # ==========================
    # Similarity Score Chart
    # ==========================
    
    # Negative values ko positive bana diya
    scores = [abs(paper["score"]) for paper in st.session_state.papers]

    paper_names = []

    for i in range(len(scores)):
        paper_names.append(f"P{i+1}")

    fig2, ax2 = plt.subplots(figsize=(3,2))

    ax2.bar(paper_names, scores)

    ax2.set_title("Similarity Score")
    ax2.set_xlabel("Papers")
    ax2.set_ylabel("Similarity")

    # Y-axis ko positive range me rakho
    ax2.set_ylim(0, max(scores) + 0.1)

    st.pyplot(fig2)


    st.markdown("---")
    st.subheader("📊 Research Gap Analysis")

    if st.button("📊 Analyze Research Gap"):
        if not st.session_state.summaries:
            st.warning("Generate at least one summary first.")
        else:
            all_summaries="\n\n".join(st.session_state.summaries.values())
            with st.spinner("Analyzing..."):
                st.session_state.analysis=analyze_papers(all_summaries)

    if st.session_state.analysis:
        st.success("✅ Research Gap Analysis Ready")
        st.markdown(st.session_state.analysis)

    st.markdown("---")
    st.subheader("📑 Final Research Report")

    if st.button("📑 Generate Final Report"):
        if not st.session_state.analysis:
            st.warning("Generate Research Gap Analysis first.")
        else:
            all_summaries="\n\n".join(st.session_state.summaries.values())
            with st.spinner("Generating report..."):
                st.session_state.report=generate_report(
                    st.session_state.topic,
                    all_summaries,
                    st.session_state.analysis
                )

if st.session_state.report:

    st.success("✅ Final Report Generated")

    st.markdown(st.session_state.report)

    # TXT Download
    st.download_button(
        label="⬇ Download Report (TXT)",
        data=st.session_state.report,
        file_name="MAARA_Final_Report.txt",
        mime="text/plain"
    )

    # Create PDF
    pdf_file = create_pdf(st.session_state.report)

    # PDF Download
    with open(pdf_file, "rb") as file:
        st.download_button(
            label="📄 Download PDF Report",
            data=file,
            file_name="MAARA_Final_Report.pdf",
            mime="application/pdf"
        )
    # DOCX Create
    docx_file = create_docx(st.session_state.report)

    # DOCX Download
    with open(docx_file, "rb") as file:

        st.download_button(
            label="📝 Download DOCX Report",
            data=file,
            file_name="MAARA_Final_Report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    
    
