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

 **Revenue by year**
   ![Revenue by Year]
   <img width="1000" height="500" alt="revenue_by_year" src="https://github.com/user-attachments/assets/b8063170-aae7-490b-b667-06744b678b87" />

 **Average playtime by genre**
   ![Average Playtime by Genre]
   <img width="1000" height="500" alt="avg_playtime_by_genre" src="https://github.com/user-attachments/assets/20ce5564-0c23-4812-a87d-a452e15aafab" />

 **Purchases by country**
   ![Purchases by Country]
   <img width="700" height="700" alt="purchases_by_country" src="https://github.com/user-attachments/assets/460b7bac-8c22-4d40-beee-4da6da284597" />

 **Top 10 games by purchases**
   ![Top 10 Games]
   <img width="1000" height="500" alt="top10_games" src="https://github.com/user-attachments/assets/2da9413b-2b89-44fb-9588-3936be4202ea" />

 **Top developers by revenue**
   ![Top Developers by Revenue]
   <img width="1000" height="500" alt="top_developers_by_revenue" src="https://github.com/user-attachments/assets/9c864ce7-0329-4751-82b9-7630259c789d" />

 **Daily purchases in last 30 days**
   ![Daily Purchases 30 Days]
   <img width="1000" height="500" alt="daily_purchases_30days" src="https://github.com/user-attachments/assets/a861aef9-405e-4bcc-99b4-9be1d786d9b0" />

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
