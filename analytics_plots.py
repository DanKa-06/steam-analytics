#!/usr/bin/env python3
"""
analytics_plots.py
- Runs diagnostic queries against your postgres DB
- Runs analytics queries, saves CSVs and an Excel workbook
- Creates 6 plots (handles empty data by saving placeholder images)
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import sys

# --- DB settings: отредактируй при необходимости ---
DB = {
    'dbname': 'steamdb',
    'user': 'steam_user',
    'password': 'steam_pass',
    'host': 'localhost',
    'port': 5432
}

OUTPUT_DIR = Path("data/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- improved queries for plotting (more meaningful than SELECT * LIMIT 10) ---
QUERIES = {
    "top10_games_by_purchases": """
        SELECT g.name,
               COALESCE(cnt.cnt, 0) AS purchases_count,
               g.positive_ratings
        FROM games g
        LEFT JOIN (
            SELECT game_id, COUNT(*) AS cnt FROM purchases GROUP BY game_id
        ) cnt ON g.game_id = cnt.game_id
        ORDER BY purchases_count DESC NULLS LAST, g.positive_ratings DESC NULLS LAST
        LIMIT 10;
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
        ORDER BY avg_playtime DESC
        LIMIT 10;
    """,
    "top_developers_by_revenue": """
        SELECT d.name AS developer, COALESCE(SUM(p.price),0) AS revenue
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
        LIMIT 15;
    """,
    "daily_purchases_30days": """
        SELECT DATE(purchase_date) AS day, COUNT(*) AS purchases
        FROM purchases
        WHERE purchase_date >= (CURRENT_DATE - INTERVAL '30 days')
        GROUP BY day
        ORDER BY day;
    """
}

DIAGNOSTIC_QUERIES = {
    "count_games": "SELECT COUNT(*) FROM games;",
    "count_purchases": "SELECT COUNT(*) FROM purchases;",
    "min_max_purchase_date": "SELECT MIN(purchase_date) AS min_date, MAX(purchase_date) AS max_date FROM purchases;",
    "price_stats": "SELECT COUNT(price) AS cnt, SUM(price) AS sum_price, AVG(price) AS avg_price FROM purchases;"
}

# --- Helpers ---
def get_engine():
    url = f"postgresql+psycopg2://{DB['user']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['dbname']}"
    return create_engine(url, echo=False)

def run_sql_to_df(sql, engine):
    try:
        return pd.read_sql(sql, engine)
    except Exception as ex:
        print("SQL read error:", ex)
        return pd.DataFrame()

def save_csv(df, name):
    file = OUTPUT_DIR / f"{name}.csv"
    df.to_csv(file, index=False, encoding="utf-8")
    print(f"[OK] Saved CSV: {file}")
    return file

def save_excel(all_dfs, filename):
    file = OUTPUT_DIR / filename
    with pd.ExcelWriter(file, engine="openpyxl") as writer:
        for name, df in all_dfs.items():
            # Excel sheet names limited to 31 chars
            sheet = name[:31]
            try:
                df.to_excel(writer, sheet_name=sheet, index=False)
            except Exception as ex:
                print(f"[WARN] Could not write sheet {sheet}: {ex}")
    print(f"[OK] Excel report saved: {file}")
    return file

def create_placeholder_image(filepath, title="No data", text="No data to plot"):
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(8,4))
    plt.text(0.5, 0.5, text, ha='center', va='center', fontsize=14)
    plt.title(title)
    plt.axis('off')
    fig.tight_layout()
    fig.savefig(filepath)
    plt.close(fig)
    print(f"[OK] Placeholder image saved: {filepath}")

# plotting helpers (matplotlib, no custom colors)
def save_line_plot(df, x_col, y_col, title, fname, xlabel=None, ylabel=None):
    file = OUTPUT_DIR / fname
    if df.empty or df[y_col].isna().all() or (df[y_col].sum() == 0):
        create_placeholder_image(file, title, "No data to plot")
        return file
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(df[x_col], df[y_col])
    ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(file)
    plt.close(fig)
    print(f"[OK] Saved: {file}")
    return file

def save_barh_plot(df, label_col, value_col, title, fname, top_n=10):
    file = OUTPUT_DIR / fname
    if df.empty or df[value_col].isna().all() or (df[value_col].sum() == 0):
        create_placeholder_image(file, title, "No data to plot")
        return file
    df_plot = df.sort_values(value_col, ascending=True).tail(top_n)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.barh(df_plot[label_col].astype(str), df_plot[value_col])
    ax.set_title(title)
    ax.set_xlabel(value_col)
    fig.tight_layout()
    fig.savefig(file)
    plt.close(fig)
    print(f"[OK] Saved: {file}")
    return file

def save_pie_plot(df, label_col, value_col, title, fname, top_n=10):
    file = OUTPUT_DIR / fname
    if df.empty or df[value_col].isna().all() or (df[value_col].sum() == 0):
        create_placeholder_image(file, title, "No data to plot")
        return file
    df_plot = df.head(top_n)
    fig, ax = plt.subplots(figsize=(7,7))
    ax.pie(df_plot[value_col], labels=df_plot[label_col].astype(str), autopct="%1.1f%%")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(file)
    plt.close(fig)
    print(f"[OK] Saved: {file}")
    return file

# --- Main ---
def main():
    engine = None
    try:
        engine = get_engine()
    except Exception as ex:
        print("Could not create engine. Check DB settings:", ex)
        sys.exit(1)

    # Diagnostics
    print("=== DIAGNOSTICS ===")
    diag_results = {}
    for name, q in DIAGNOSTIC_QUERIES.items():
        df = run_sql_to_df(q, engine)
        print(f"{name}:")
        print(df)
        diag_results[name] = df

    # Run analytics queries, save CSVs and collect for Excel
    all_results = {}
    for name, q in QUERIES.items():
        df = run_sql_to_df(q, engine)
        save_csv(df, name)
        all_results[name] = df

    # Save to Excel
    save_excel(all_results, "report.xlsx")

    # PLOTS (6 required)
    # 1) revenue_by_year
    if "revenue_by_year" in QUERIES:
        rev_df = run_sql_to_df(QUERIES["revenue_by_year"], engine)
    else:
        rev_df = pd.DataFrame()
    # ensure year is string or datetime for plotting
    if not rev_df.empty and 'year' in rev_df.columns:
        rev_df['year'] = pd.to_datetime(rev_df['year']).dt.year
    save_line_plot(rev_df, 'year', 'total_revenue', "Revenue by Year", "revenue_by_year.png", xlabel="Year", ylabel="Total revenue")

    # 2) avg_playtime_by_genre
    play_df = run_sql_to_df(QUERIES["avg_playtime_by_genre"], engine)
    save_barh_plot(play_df, 'genre', 'avg_playtime', "Avg Playtime by Genre (top 10)", "avg_playtime_by_genre.png")

    # 3) purchases_by_country (pie)
    country_df = run_sql_to_df(QUERIES["purchases_by_country"], engine)
    save_pie_plot(country_df, 'country', 'purchases', "Purchases by Country (top 15)", "purchases_by_country.png")

    # 4) top10_games_by_purchases
    top10_df = run_sql_to_df(QUERIES["top10_games_by_purchases"], engine)
    # prefer purchases_count if present, else positive_ratings
    if not top10_df.empty and 'purchases_count' in top10_df.columns and top10_df['purchases_count'].sum() > 0:
        save_barh_plot(top10_df, 'name', 'purchases_count', "Top 10 Games by Purchases", "top10_games.png", top_n=10)
    else:
        # fallback to positive_ratings
        if not top10_df.empty and 'positive_ratings' in top10_df.columns:
            save_barh_plot(top10_df, 'name', 'positive_ratings', "Top 10 Games by Positive Ratings (fallback)", "top10_games.png", top_n=10)
        else:
            create_placeholder_image(OUTPUT_DIR / "top10_games.png", "Top10 Games", "No data to plot")

    # 5) top_developers_by_revenue
    dev_df = run_sql_to_df(QUERIES["top_developers_by_revenue"], engine)
    save_barh_plot(dev_df, 'developer', 'revenue', "Top Developers by Revenue (top 10)", "top_developers_by_revenue.png")

    # 6) daily_purchases_30days
    daily_df = run_sql_to_df(QUERIES["daily_purchases_30days"], engine)
    save_line_plot(daily_df, 'day', 'purchases', "Daily Purchases (last 30 days)", "daily_purchases_30days.png", xlabel="Day", ylabel="Purchases")

    print("=== DONE ===")

if __name__ == "__main__":
    main()
