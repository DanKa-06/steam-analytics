import psycopg2
import pandas as pd
from pathlib import Path

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
    "games_per_developer": """
        SELECT d.name AS developer, COUNT(g.game_id) AS games_count
        FROM games g
        JOIN developers d ON g.developer_id = d.developer_id
        GROUP BY d.name
        ORDER BY games_count DESC
        LIMIT 10;
    """,
    "top_games_by_purchases": """
        SELECT g.name, COUNT(p.purchase_id) AS purchases_count
        FROM purchases p
        JOIN games g ON p.game_id = g.game_id
        GROUP BY g.name
        ORDER BY purchases_count DESC
        LIMIT 10;
    """,
    "top_selling_games": """
        SELECT g.name, COUNT(p.purchase_id) AS sales
        FROM purchases p
        JOIN games g ON p.game_id = g.game_id
        GROUP BY g.name
        ORDER BY sales DESC
        LIMIT 10;
    """,
    "revenue_by_year": """
        SELECT DATE_TRUNC('year', purchase_date) AS year, SUM(price) AS total_revenue
        FROM purchases
        GROUP BY year
        ORDER BY year;
    """,
    "avg_price_by_platform": """
        SELECT pl.name AS platform, AVG(p.price) AS avg_price
        FROM purchases p
        JOIN game_platforms gp ON p.game_id = gp.game_id
        JOIN platforms pl ON gp.platform_id = pl.platform_id
        GROUP BY pl.name
        ORDER BY avg_price DESC;
    """,
    "avg_playtime_by_genre": """
        SELECT ge.name AS genre, AVG(g.average_playtime) AS avg_playtime
        FROM game_genres gg
        JOIN genres ge ON gg.genre_id = ge.genre_id
        JOIN games g ON gg.game_id = g.game_id
        GROUP BY ge.name
        ORDER BY avg_playtime DESC;
    """,
    "top_developers_by_revenue": """
        SELECT d.name AS developer, SUM(p.price) AS revenue
        FROM purchases p
        JOIN games g ON p.game_id = g.game_id
        JOIN developers d ON g.developer_id = d.developer_id
        GROUP BY d.name
        ORDER BY revenue DESC
        LIMIT 10;
    """,
    "purchases_by_country": """
        SELECT u.country, COUNT(p.purchase_id) AS purchases
        FROM purchases p
        JOIN users u ON p.user_id = u.user_id
        GROUP BY u.country
        ORDER BY purchases DESC
        LIMIT 10;
    """,
    "avg_rating_by_genre": """
        SELECT ge.name AS genre, AVG(r.rating) AS avg_rating
        FROM reviews r
        JOIN games g ON r.game_id = g.game_id
        JOIN game_genres gg ON gg.game_id = g.game_id
        JOIN genres ge ON gg.genre_id = ge.genre_id
        GROUP BY ge.name
        ORDER BY avg_rating DESC
        LIMIT 10;
    """,
    "highest_pos_neg_ratio": """
        SELECT name, positive_ratings, negative_ratings,
          CASE WHEN negative_ratings = 0 THEN positive_ratings 
               ELSE (positive_ratings::float / negative_ratings) END AS pos_neg_ratio
        FROM games
        WHERE positive_ratings IS NOT NULL
        ORDER BY pos_neg_ratio DESC
        LIMIT 15;
    """,
    "daily_purchases_30days": """
        SELECT DATE(purchase_date) AS day, COUNT(*) AS purchases
        FROM purchases
        WHERE purchase_date >= (CURRENT_DATE - INTERVAL '30 days')
        GROUP BY day
        ORDER BY day;
    """,
    "price_buckets_vs_playtime": """
        SELECT width_bucket(g.price, 0, 60, 6) AS price_bucket,
               MIN(g.price) AS min_price, MAX(g.price) AS max_price,
               AVG(g.average_playtime) AS avg_playtime,
               COUNT(*) AS games_count
        FROM games g
        GROUP BY price_bucket
        ORDER BY price_bucket;
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
