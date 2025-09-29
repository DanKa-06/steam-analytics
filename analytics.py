import psycopg2
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

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
    """,
    "purchases_by_country": """
        SELECT u.country, COUNT(p.purchase_id) AS purchases
        FROM purchases p
        JOIN users u ON p.user_id = u.user_id
        GROUP BY u.country
        ORDER BY purchases DESC
        LIMIT 10;
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
    "daily_purchases_30days": """
        SELECT DATE(purchase_date) AS day, COUNT(*) AS purchases
        FROM purchases
        WHERE purchase_date >= (CURRENT_DATE - INTERVAL '30 days')
        GROUP BY day
        ORDER BY day;
    """
}

def run_query(name, sql, conn):
    df = pd.read_sql(sql, conn)
    file = OUTPUT_DIR / f"{name}.csv"
    df.to_csv(file, index=False, encoding="utf-8")
    print(f"[OK] Saved CSV: {file}")
    return df

def save_excel(results, output_dir):
    file = output_dir / "report.xlsx"
    with pd.ExcelWriter(file, engine="openpyxl") as writer:
        for name, df in results.items():
            df.to_excel(writer, sheet_name=name[:30], index=False)
    print(f"[OK] Excel report saved: {file}")

# ---- Plotting functions ----
def plot_revenue_by_year(df):
    plt.figure(figsize=(8,5))
    df["year"] = pd.to_datetime(df["year"]).dt.year
    plt.plot(df['year'], df['total_revenue'], marker='o')
    plt.title("Revenue by Year")
    plt.xlabel("Year")
    plt.ylabel("Revenue ($)")
    plt.grid(True)
    plt.savefig(OUTPUT_DIR / "revenue_by_year.png")
    plt.close()

def plot_avg_playtime_by_genre(df):
    plt.figure(figsize=(10,6))
    df = df.sort_values("avg_playtime", ascending=False).head(10)
    plt.barh(df['genre'], df['avg_playtime'])
    plt.title("Avg Playtime by Genre (Top 10)")
    plt.xlabel("Playtime (hours)")
    plt.ylabel("Genre")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "avg_playtime_by_genre.png")
    plt.close()

def plot_purchases_by_country(df):
    plt.figure(figsize=(8,6))
    plt.pie(df['purchases'], labels=df['country'], autopct='%1.1f%%', startangle=140)
    plt.title("Purchases by Country (Top 10)")
    plt.savefig(OUTPUT_DIR / "purchases_by_country.png")
    plt.close()

def plot_top10_games(df):
    plt.figure(figsize=(10,6))
    if "name" in df.columns:
        plt.barh(df['name'], range(len(df)))
        plt.title("Top 10 Games (Sample)")
        plt.xlabel("Index")
        plt.ylabel("Game")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "top10_games.png")
    plt.close()

def plot_top_developers_by_revenue(df):
    plt.figure(figsize=(10,6))
    plt.barh(df['developer'], df['revenue'])
    plt.title("Top Developers by Revenue")
    plt.xlabel("Revenue ($)")
    plt.ylabel("Developer")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "top_developers_by_revenue.png")
    plt.close()

def plot_daily_purchases(df):
    plt.figure(figsize=(8,5))
    df["day"] = pd.to_datetime(df["day"])
    plt.plot(df["day"], df["purchases"], marker="o")
    plt.title("Daily Purchases (Last 30 days)")
    plt.xlabel("Day")
    plt.ylabel("Purchases")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "daily_purchases_30days.png")
    plt.close()

# ---- Main ----
if __name__ == "__main__":
    conn = psycopg2.connect(**DB)
    results = {}
    for name, sql in queries.items():
        df = run_query(name, sql, conn)
        results[name] = df

        # build plots
        if name == "revenue_by_year":
            plot_revenue_by_year(df)
        elif name == "avg_playtime_by_genre":
            plot_avg_playtime_by_genre(df)
        elif name == "purchases_by_country":
            plot_purchases_by_country(df)
        elif name == "top10_games":
            plot_top10_games(df)
        elif name == "top_developers_by_revenue":
            plot_top_developers_by_revenue(df)
        elif name == "daily_purchases_30days":
            plot_daily_purchases(df)

    conn.close()
    save_excel(results, OUTPUT_DIR)
