import arxiv

# Create client
client = arxiv.Client()

# Search for papers
search = arxiv.Search(
    query="Multi-Agent Systems",
    max_results=1
)

# Print first paper
for paper in client.results(search):
    print("Title:", paper.title)
    print("Authors:", ", ".join(author.name for author in paper.authors))
    print("Published:", paper.published)
    print("Abstract:", paper.summary)
    print("PDF Link:", paper.pdf_url)


"""import arxiv
import pandas as pd

# Create client
client = arxiv.Client()

# Search for 30 papers
search = arxiv.Search(
    query="Multi-Agent Systems",
    max_results=30
)

papers = []

# Fetch papers
for paper in client.results(search):
    papers.append({
        "Title": paper.title,
        "Authors": ", ".join(author.name for author in paper.authors),
        "Year": paper.published.year,
        "Abstract": paper.summary,
        "PDF Link": paper.pdf_url
    })

# Convert to DataFrame
df = pd.DataFrame(papers)

# Save CSV
df.to_csv("papers.csv", index=False)

print("CSV Created Successfully!")
print(df.head())"""