# IMDB Analysis: Serbian and Yugoslav Films

Analysis of movies from Serbia and Yugoslavia across history using Python (Pandas & Matplotlib).
The goal is to explore trends, top-rated movies and directors, and the most popular genres by decade.

## Data
This project uses the [IMDB Extensive Dataset](https://www.kaggle.com/datasets/simhyunsu/imdbextensivedataset) from Kaggle.  
Download the dataset and place the movie-level CSV in the project root as `IMDB.csv` (or adjust the script path).

## Technologies
- **Python 3**
- **Pandas** (data processing)
- **Matplotlib** (visualization)

## Main Analysis Steps
1. **Load & clean data**
   - Remove unused columns (budget, description, etc.)
   - Filter movies from Serbia/Yugoslavia
   - Convert numeric fields (year, ratings, votes)
2. **Director analysis**
   - Film count per director
   - Average rating per director (for those with more than 3 films)
   - Top 10 directors by average rating
3. **Decade analysis**
   - Assign a decade to each film
   - Split multi-valued genres (films often have several)
   - Build a pivot table: number of films per **genre × decade**
4. **Visualization**
   - Horizontal bar chart: **Top 10 directors** by rating

## Results

The analysis produces the following outputs:

- **Genre × Decade table** → saved as `pivot_genre_by_decade.csv`.
  - Rows are decades (e.g., 1960, 1970, …), columns are genres (Drama, Comedy, …).
  - Each cell is the **count of films** tagged with that genre in that decade.
  - Note: a film with multiple genres contributes once to **each** of its listed genres.

- **Directors summary (printed to console)** → `broj_po_reziseru3` table:
  - `director` — director name  
  - `broj_filmova` — number of films  
  - `prosek_ocena` — average IMDB rating  
  - `broj_glasova` — total votes  
  - `najraniji_film` / `najkasniji_film` — earliest/latest film year  
  - `period_stvaranja` — active span (`latest - earliest`)  
  - Filtered to directors with **> 3 films**, sorted by `prosek_ocena`.

- **Top 10 Directors chart** → displayed in a window:
  - Horizontal bar chart of the **Top 10 directors by average rating** (after the “> 3 films” filter).
  - You can optionally save it (e.g., `outputs/top10_directors.png`).

- **Quick console sanity checks**:
  - Year range of the dataset (min/max).
  - Top-rated titles (largest `avg_vote`).
  - Films with `avg_vote > 8.1` (sorted by rating, then votes).

> Interpretation: Use `pivot_genre_by_decade.csv` to see which genres dominate each decade.  
> Use the directors summary and chart to spot consistently high-rated directors with a meaningful body of work.


## How to Run
1. Place `IMDB.csv` next to your Python script (or notebook).
2. Install dependencies:
   ```bash
   pip install pandas matplotlib
   ```
3. Run the analysis (script version):
   ```bash
   python imdb_analysis.py
   ```
   A CSV with the **genre × decade** pivot will be saved, and a chart of the **Top 10 directors** will be shown.

## Notes
- Uses a local `IMDB.csv` from the Kaggle dataset (not included).
- Deduplicates by `imdb_title_id`.
- `country` filter allows mixed entries (e.g., “Serbia, France”).
- Genres are split by `, `; multi-genre films count once per genre.
- Outputs: saves `pivot_genre_by_decade.csv` and shows a Top-10 directors chart.


## Suggested Files
```
IMDB.csv
imdb_analysis.py
outputs/            # optional (for saved CSV/PNG)
README.md
```

## License
MIT (or your preferred license).
