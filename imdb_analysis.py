import pandas as pd
import matplotlib.pyplot as plt

# 1) Load CSV
imdb = pd.read_csv("IMDB.csv")
print(imdb.head())

# 2) Define columns to drop 

# "imdb_title_id"

cols_to_drop = [
    "budget", "language", "duration", "production_company",
    "actors", "description", "writer", "date_published", "usa_gross_income",
    "worlwide_gross_income", "reviews_from_users", "reviews_from_critics", "metascore"
]

# Drop unused columns (ignore missing columns if any)
imdb_cl = imdb.drop(columns=cols_to_drop, errors="ignore")

# 3) Normalize country to lowercase (for robust matching)
imdb_cl["country"] = imdb_cl["country"].str.lower()

# 4) Filter rows that contain Serbia or Yugoslavia in the country field

mask = (
    imdb_cl["country"].str.contains("serbia", na=False) |
    imdb_cl["country"].str.contains("yugoslavia", na=False)
)
serbia = imdb_cl[mask].drop_duplicates(subset=["imdb_title_id"]).reset_index(drop=True)

print(serbia.columns)

# 5) Ensure numeric types for key columns
serbia["year"] = pd.to_numeric(serbia["year"], errors="coerce")
serbia["avg_vote"] = pd.to_numeric(serbia["avg_vote"], errors="coerce")
serbia["votes"] = pd.to_numeric(serbia["votes"], errors="coerce") 

# Quick sanity checks
print(serbia["year"].min())
print(serbia["year"].max())
print(serbia.nlargest(10, "avg_vote"))

# 6) Sort by rating then votes (highest first) and show where avg_vote > 8.1
glasovi = serbia.sort_values(ascending=False, by=["avg_vote", "votes"])
print(glasovi[glasovi["avg_vote"] > 8.1])

# 7) Directors: simple frequency table (>10 films)
broj_po_reziseru = serbia["director"].value_counts()
print(broj_po_reziseru[broj_po_reziseru > 10])

# Count films per director
broj_po_reziseru1 = (
    serbia.groupby("director")["imdb_title_id"]
    .count()
    .reset_index()
    .sort_values(by="imdb_title_id", ascending=False)
)

# Sum of avg_vote per director (later used to compute mean)
broj_po_reziseru2 = (
    serbia.groupby("director")["avg_vote"]
    .sum()
    .reset_index()
    .sort_values(by="avg_vote", ascending=False)
)

# Average rating per director

broj_po_reziseru3 = (
    serbia.groupby("director")
    .agg(
        broj_filmova=("imdb_title_id", "count"),
        prosek_ocena=("avg_vote", "mean"),
        broj_glasova=("votes", "sum"),
        najraniji_film=("year", "min"),
        najkasniji_film=("year", "max"),
    )
    .reset_index()
    .sort_values(by="prosek_ocena", ascending=False)
    .round(2)
)
broj_po_reziseru3["period_stvaranja"] = (
    broj_po_reziseru3["najkasniji_film"] - broj_po_reziseru3["najraniji_film"]
)
broj_po_reziseru3 = broj_po_reziseru3[broj_po_reziseru3["broj_filmova"] > 3]
print(broj_po_reziseru3.head(20))

# 8) Decade
serbia["decade"] = (serbia["year"] // 10) * 10
print(serbia["decade"].unique())

# 9) Split genre into multiple columns (", " as delimiter), then build long and crosstab
serbia = serbia.join(
    serbia["genre"].str.split(r",\s*", expand=True).add_prefix("genre_")
)

genre_cols = sorted(
    [c for c in serbia.columns if c.startswith("genre_")],
    key=lambda x: int(x.split("_")[1])
)

long = (
    serbia.melt(
        id_vars="decade",
        value_vars=genre_cols,
        var_name="_src",
        value_name="_genre",
    )
    .dropna(subset=["_genre"])
)
long["_genre"] = long["_genre"].str.strip()

pivot = pd.crosstab(long["decade"], long["_genre"])
print(pivot)

# 10) Save pivot to CSV (UTF-8 with BOM for Excel compatibility on Windows)
pivot.to_csv("pivot_genre_by_decade.csv", index=True, encoding="utf-8-sig")

# 11) Simple bar chart: Top 10 directors by average rating (from broj_po_reziseru3)
top_directors = broj_po_reziseru3.head(10)
plt.barh(top_directors["director"], top_directors["prosek_ocena"])
plt.xlabel("Prosečna ocena")  
plt.title("Top 10 režisera iz Srbije")
plt.tight_layout()           
plt.show()
