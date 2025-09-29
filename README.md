# QuickPlay Analytics (Steam Dataset)

**QuickPlay Analytics** — analytics project on Steam games (games, developers, publishers, genres, platforms).
This repo contains SQL schema & transformation scripts, a set of analytic SQL queries, a small Python script to run those queries and export results, a synthetic-data generator, and a visualization script that saves results both as CSV/Excel and PNG charts.

> **Important** — I attempted to set up Apache Superset (for dashboards) during the work, but hit environment / dependency issues (missing `flask_cors`, `marshmallow_enum`, and an incompatibility with `marshmallow` that caused Alembic migrations to fail). To finish the assignment reliably I skipped the Superset dashboard part and delivered everything using PostgreSQL (pgAdmin/psql) + Python only.

---

## Repository layout

```
.
├─ data/steam.csv                 # Original dataset (NOT included - download from Kaggle)
├─ sql/
│  ├─ create_schema.sql           # schema (normalized tables)
│  ├─ create_raw_table.sql        # raw/staging table(s)
│  └─ transform_from_raw.sql      # transforms from raw -> normalized tables
├─ queries/
│  └─ queries.sql                 # 10 analytics queries + basic checks (each query commented)
├─ scripts/
│  └─ generate_synthetic.py       # generate synthetic users / purchases / reviews
├─ main.py                        # run selected queries and export CSV (uses DB connection)
├─ analytics_plots.py             # extended runner: saves CSV + Excel + plots
├─ output/                        # CSV, Excel, and PNG results (ignored in git)
├─ screenshot.png                 # placeholder screenshot for analytics
├─ requirements.txt               # Python deps
└─ README.md                      # this file
```

Dataset: [Steam Store Games on Kaggle](https://www.kaggle.com/datasets/nikdavis/steam-store-games?resource=download)
**Note:** `data/steam.csv` is *not* included in the repo (Kaggle dataset license / size). Download it and place it at `data/steam.csv` before running the ingestion step.

---

## Prerequisites

* PostgreSQL (e.g., installed with pgAdmin) — tested with a local PostgreSQL server
* Python 3.10+ (create & use a virtual environment)
* `psql` command-line client (or use pgAdmin)
* Git (for pushing to GitHub)

---

## Quickstart — local setup

1. **Create DB user & database (example)**

   ```sql
   CREATE USER steam_user WITH PASSWORD 'steam_pass';
   CREATE DATABASE steamdb OWNER steam_user;
   ```

2. **Place the dataset**
   Download the Steam dataset and save as:

   ```
   data/steam.csv
   ```

3. **Create virtual env & install Python deps**

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

4. **Load DB schema and staging tables**

   ```powershell
   psql -h localhost -U steam_user -d steamdb -f sql/create_schema.sql
   psql -h localhost -U steam_user -d steamdb -f sql/create_raw_table.sql
   ```

5. **Import CSV into raw table**

   ```powershell
   psql -h localhost -U steam_user -d steamdb -c "\copy raw_steam FROM 'data/steam.csv' CSV HEADER;"
   ```

6. **Run transform SQL to populate normalized tables**

   ```powershell
   psql -h localhost -U steam_user -d steamdb -f sql/transform_from_raw.sql
   ```

7. **Run analytic queries**

   * Run via psql:

     ```powershell
     psql -h localhost -U steam_user -d steamdb -f queries/queries.sql
     ```
   * Or via Python:

     ```powershell
     $env:DATABASE_URL = "postgresql+psycopg2://steam_user:steam_pass@localhost:5432/steamdb"
     python main.py
     ```

8. **Generate synthetic data (optional)**

   ```powershell
   python scripts/generate_synthetic.py
   ```

9. **Run extended analytics with plots + Excel**

   ```powershell
   python analytics_plots.py
   ```

---

## Visualizations

The script `analytics_plots.py` generates **6 charts** in `output/`:

1. **Revenue by year**
   ![Revenue by Year](output/revenue_by_year.png)

2. **Average playtime by genre**
   ![Average Playtime by Genre](output/avg_playtime_by_genre.png)

3. **Purchases by country**
   ![Purchases by Country](output/purchases_by_country.png)

4. **Top 10 games by purchases**
   ![Top 10 Games](output/top10_games.png)

5. **Top developers by revenue**
   ![Top Developers by Revenue](output/top_developers_by_revenue.png)

6. **Daily purchases in last 30 days**
   ![Daily Purchases 30 Days](output/daily_purchases_30days.png)

Additionally, all results are exported to:

* Individual CSVs (`output/*.csv`)
* Combined Excel report (`output/report.xlsx`)

---

## GitHub upload instructions

(… section preserved from previous README …)

---

## Notes about Superset

(… section preserved from previous README …)

---

## Final notes (what I completed)

* SQL schema and raw table DDL scripts
* Transformation into normalized schema
* Ten analytic queries with comments
* Synthetic data generator
* Two Python runners: `main.py` (CSV only), `analytics_plots.py` (CSV + Excel + plots)
* Six visualizations as PNG files
* README with setup & GitHub instructions
