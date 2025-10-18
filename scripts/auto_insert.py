import psycopg2
import random
import time
from datetime import datetime

# --- Настройки подключения к БД ---
DB = {
    "dbname": "steamdb",
    "user": "steam_user",
    "password": "steam_pass",
    "host": "localhost",
    "port": 5432
}

def insert_random_purchase():
    try:
        conn = psycopg2.connect(**DB)
        cur = conn.cursor()

        # Выбираем случайного пользователя и игру
        cur.execute("SELECT user_id FROM users ORDER BY RANDOM() LIMIT 1;")
        user_id = cur.fetchone()[0]

        cur.execute("SELECT game_id, price FROM games ORDER BY RANDOM() LIMIT 1;")
        game_id, price = cur.fetchone()

        # Создаём новую покупку
        purchase_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("""
            INSERT INTO purchases (user_id, game_id, price, purchase_date)
            VALUES (%s, %s, %s, %s);
        """, (user_id, game_id, price, purchase_date))

        conn.commit()
        print(f"[{purchase_date}] Inserted purchase: user={user_id}, game={game_id}, price={price}")

    except Exception as e:
        print("Error inserting data:", e)

    finally:
        if conn:
            cur.close()
            conn.close()


if __name__ == "__main__":
    print("Auto data insertion started (press Ctrl+C to stop)")
    while True:
        insert_random_purchase()
        time.sleep(10)  # каждые 10 секунд добавляет запись
