import psycopg2
import pandas as pd
from pathlib import Path

# DB settings
DB = {
    'dbname': 'steamdb',
    'user': 'steam_user',
    'password': 'steam_pass',
    'host': 'localhost',
    'port': 5432
}

OUTPUT_DIR = Path("data/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

queries = {
    "top10_games": """
        SELECT * FROM games LIMIT 10;
    """,
    "games_after_2018": """
        SELECT name, release_date, positive_ratings 
        FROM games
        WHERE release_date >= '2018-01-01'
        ORDER BY positive_ratings DESC
        LIMIT 20;
    """,
    "revenue_by_year": """
        SELECT DATE_TRUNC('year', purchase_date) AS year, SUM(price) AS total_revenue
        FROM purchases
        GROUP BY year
        ORDER BY year;
    """,
    "avg_playtime_by_genre": """
        SELECT ge.name AS genre, AVG(g.average_playtime) AS avg_playtime
        FROM game_genres gg
        JOIN genres ge ON gg.genre_id = ge.genre_id
        JOIN games g ON gg.game_id = g.game_id
        GROUP BY ge.name
        ORDER BY avg_playtime DESC;
    """
}

def run_query(name, sql, conn):
    df = pd.read_sql(sql, conn)
    file = OUTPUT_DIR / f"{name}.csv"
    df.to_csv(file, index=False, encoding="utf-8")
    print(f"[OK] Saved: {file}")

if __name__ == "__main__":
    conn = psycopg2.connect(**DB)
    for name, sql in queries.items():
        run_query(name, sql, conn)
    conn.close()
