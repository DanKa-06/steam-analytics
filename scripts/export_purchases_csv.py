import psycopg2
import pandas as pd
from datetime import datetime

DB = {
    "dbname": "steamdb",
    "user": "steam_user",
    "password": "steam_pass",
    "host": "localhost",
    "port": 5432
}

# Подключаемся к базе
conn = psycopg2.connect(**DB)

# Выполняем запрос
query = """
SELECT 
    DATE(purchase_date) AS date,
    COUNT(*) AS total_purchases
FROM purchases
GROUP BY date
ORDER BY date;
"""

df = pd.read_sql(query, conn)

# Приводим типы данных к корректным
df["date"] = pd.to_datetime(df["date"], errors="coerce")  # тип datetime64[ns]
df["total_purchases"] = df["total_purchases"].astype(int)  # тип int64

# Сохраняем в CSV в правильном формате
df.to_csv("purchases_snapshot.csv", index=False, date_format="%Y-%m-%d")

conn.close()

print("✅ CSV-файл purchases_snapshot.csv успешно создан с правильными типами данных.")
print(df.dtypes)
