# QuickPlay Analytics (Steam Dataset)

## Company
**QuickPlay Analytics** — we analyze Steam games, purchases and player behavior to provide insights for product managers and marketers.

## Project overview
This project ingests a Steam games dataset, normalizes the data (games, developers, publishers, genres, platforms), simulates user purchases and reviews, and produces analytics (top sellers, revenue trends, genre playtime, etc.).

## Files
- `data/steam.csv` - original dataset (not included; download from Kaggle)
- `sql/create_raw_table.sql`
- `sql/create_schema.sql`
- `sql/transform_from_raw.sql`
- `queries/queries.sql` - 10 analytics + basic checks
- `scripts/generate_synthetic.py` - generate users & purchases
- `main.py` - run selected queries and export CSV
- `output/` - generated CSV results
- `screenshot.png` - placeholder for analytics screenshot

## How to run (step-by-step)
1. Install PostgreSQL and create the database:
   ```sql
   CREATE USER steam_user WITH PASSWORD 'steam_pass';
   CREATE DATABASE steamdb OWNER steam_user;
