CREATE TABLE IF NOT EXISTS developers (
  developer_id SERIAL PRIMARY KEY,
  name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS publishers (
  publisher_id SERIAL PRIMARY KEY,
  name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS games (
  game_id SERIAL PRIMARY KEY,
  app_id INTEGER UNIQUE,
  name TEXT,
  release_date DATE,
  developer_id INTEGER REFERENCES developers(developer_id),
  publisher_id INTEGER REFERENCES publishers(publisher_id),
  price NUMERIC(10,2),
  average_playtime INTEGER,
  positive_ratings INTEGER,
  negative_ratings INTEGER
);

CREATE TABLE IF NOT EXISTS genres (
  genre_id SERIAL PRIMARY KEY,
  name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS platforms (
  platform_id SERIAL PRIMARY KEY,
  name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS game_genres (
  game_id INTEGER REFERENCES games(game_id),
  genre_id INTEGER REFERENCES genres(genre_id),
  PRIMARY KEY (game_id, genre_id)
);

CREATE TABLE IF NOT EXISTS game_platforms (
  game_id INTEGER REFERENCES games(game_id),
  platform_id INTEGER REFERENCES platforms(platform_id),
  PRIMARY KEY (game_id, platform_id)
);

CREATE TABLE IF NOT EXISTS users (
  user_id SERIAL PRIMARY KEY,
  username TEXT,
  country TEXT,
  registration_date DATE
);

CREATE TABLE IF NOT EXISTS purchases (
  purchase_id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(user_id),
  game_id INTEGER REFERENCES games(game_id),
  purchase_date TIMESTAMP,
  price NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS reviews (
  review_id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(user_id),
  game_id INTEGER REFERENCES games(game_id),
  rating INTEGER,
  review_text TEXT,
  review_date TIMESTAMP
);
