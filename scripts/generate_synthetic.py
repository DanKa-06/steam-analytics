import random
from faker import Faker
import csv
from datetime import datetime, timedelta
import psycopg2

fake = Faker()
F = 5000  # number of users to generate
P = 50000  # number of purchases to generate

# DB settings
DB = {
    'dbname': 'steamdb',
    'user': 'steam_user',
    'password': 'steam_pass',
    'host': 'localhost',
    'port': 5432
}

conn = psycopg2.connect(**DB)
cur = conn.cursor()

# 1) generate users
cur.execute("SELECT COUNT(*) FROM users")
count = cur.fetchone()[0]
if count == 0:
    for i in range(F):
        username = fake.user_name() + str(random.randint(0,9999))
        country = fake.country_code()
        reg_date = fake.date_between(start_date='-5y', end_date='today')
        cur.execute(
            "INSERT INTO users (username, country, registration_date) VALUES (%s,%s,%s)",
            (username, country, reg_date)
        )
    conn.commit()
    print("Inserted users:", F)

# 2) get game_ids for purchases
cur.execute("SELECT game_id FROM games")
game_ids = [r[0] for r in cur.fetchall()]

cur.execute("SELECT user_id FROM users")
user_ids = [r[0] for r in cur.fetchall()]

# 3) generate purchases
for i in range(P):
    user = random.choice(user_ids)
    game = random.choice(game_ids)
    days_ago = random.randint(0, 365*3)
    purchase_date = datetime.now() - timedelta(days=days_ago, hours=random.randint(0,23))
    price = round(random.choice([0.0, 0.99, 4.99, 9.99, 14.99, 19.99, 29.99, 49.99]),2)
    cur.execute(
        "INSERT INTO purchases (user_id, game_id, purchase_date, price) VALUES (%s,%s,%s,%s)",
        (user, game, purchase_date, price)
    )
    if i % 2000 == 0:
        conn.commit()
conn.commit()
print("Inserted purchases:", P)
cur.close()
conn.close()
