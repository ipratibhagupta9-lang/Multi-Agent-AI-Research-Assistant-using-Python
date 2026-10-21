import pandas as pd

# Load dataset
df = pd.read_csv("papers.csv")

print("Before Cleaning:", df.shape)

# Remove duplicate papers
df = df.drop_duplicates()

# Remove rows where Title or Abstract is missing
df = df.dropna(subset=["Title", "Abstract"])

print("After Cleaning:", df.shape)

# Save cleaned dataset
df.to_csv("clean_papers.csv", index=False)

print("Clean dataset saved successfully!")