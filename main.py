from search_agent import search_papers
from summarization_agent import summarize_text
from critic_agent import analyze_papers
from report_writer import generate_report
#from docx_generator import create_docx
from maara_docx import create_docx
#from pdf_generator import create_pdf
from maara_pdf import create_pdf

# ==============================
# User Input
# ==============================

topic = input("Enter Research Topic: ")

# ==============================
# Search Papers
# ==============================

papers = search_papers(topic)

all_summaries = []

print("\n" + "=" * 70)
print("TOP 5 RESEARCH PAPERS")
print("=" * 70)

# ==============================
# Generate Summary for Each Paper
# ==============================

for i, paper in enumerate(papers):

    print(f"\n📄 PAPER {i+1}")
    print("-" * 70)

    print("Title :", paper["title"])
    print("Year :", paper["year"])
    print("Similarity Score :", paper["score"])

    print("\nGenerating Summary...\n")

    summary = summarize_text(paper["abstract"])

    all_summaries.append(summary)

    print(summary)

    print("=" * 70)

# ==============================
# Critic Agent
# ==============================

print("\n")
print("=" * 70)
print("RESEARCH GAP ANALYSIS")
print("=" * 70)

combined_summary = "\n\n".join(all_summaries)

analysis = analyze_papers(combined_summary)

print(analysis)

# ==============================
# Report Writer
# ==============================

print("\n")
print("=" * 70)
print("GENERATING FINAL RESEARCH REPORT")
print("=" * 70)

report = generate_report(
    topic,
    combined_summary,
    analysis
)

print(report)

print("\n" + "=" * 70)
print("CHECK: GENERATED REPORT")
print("=" * 70)
print(report[:1500])
print("=" * 70)

# ==============================
# Save TXT Report
# ==============================

with open("research_report.txt", "w", encoding="utf-8") as file:
    file.write(report)

print("\n✅ TXT Report Saved")

# ==============================
# Save DOCX Report
# ==============================

docx_file = create_docx(report)

print(f"✅ DOCX Report Saved: {docx_file}")

# ==============================
# Save PDF Report
# ==============================

pdf_file = create_pdf(report)

print(f"✅ PDF Report Saved: {pdf_file}")

# ==============================
# Finished
# ==============================

print("\n" + "=" * 70)
print("🎉 MAARA COMPLETED SUCCESSFULLY")
print("=" * 70)

