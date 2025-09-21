-- ===== Fill developers =====
INSERT INTO developers (name)
SELECT DISTINCT developer
FROM raw_games
WHERE developer IS NOT NULL AND developer <> ''
ON CONFLICT (name) DO NOTHING;

-- ===== Fill publishers =====
INSERT INTO publishers (name)
SELECT DISTINCT publisher
FROM raw_games
WHERE publisher IS NOT NULL AND publisher <> ''
ON CONFLICT (name) DO NOTHING;

-- ===== Fill genres =====
WITH exploded AS (
  SELECT DISTINCT trim(unnest(string_to_array(genres, ';'))) AS g
  FROM raw_games
  WHERE genres IS NOT NULL
)
INSERT INTO genres (name)
SELECT g
FROM exploded
WHERE g <> ''
ON CONFLICT (name) DO NOTHING;

-- ===== Fill platforms =====
WITH exploded AS (
  SELECT DISTINCT trim(unnest(string_to_array(platforms, ';'))) AS p
  FROM raw_games
  WHERE platforms IS NOT NULL
)
INSERT INTO platforms (name)
SELECT p
FROM exploded
WHERE p <> ''
ON CONFLICT (name) DO NOTHING;

-- ===== Fill games =====
INSERT INTO games (app_id, name, release_date, developer_id, publisher_id, price,
                   average_playtime, positive_ratings, negative_ratings)
SELECT
  rg.app_id,
  rg.name,
  rg.release_date,
  d.developer_id,
  p.publisher_id,
  NULLIF(rg.price, 0)::numeric,
  rg.average_playtime,
  rg.positive_ratings,
  rg.negative_ratings
FROM raw_games rg
LEFT JOIN developers d ON rg.developer = d.name
LEFT JOIN publishers p ON rg.publisher = p.name
ON CONFLICT (app_id) DO NOTHING;


-- ===== Fill game_genres (many-to-many) =====
WITH t AS (
  SELECT g.game_id, trim(unnest(string_to_array(rg.genres, ';'))) AS genre_name
  FROM raw_games rg
  JOIN games g ON rg.app_id = g.app_id
  WHERE rg.genres IS NOT NULL
)
INSERT INTO game_genres (game_id, genre_id)
SELECT t.game_id, ge.genre_id
FROM t
JOIN genres ge ON ge.name = t.genre_name
ON CONFLICT DO NOTHING;

-- ===== Fill game_platforms (many-to-many) =====
WITH t AS (
  SELECT g.game_id, trim(unnest(string_to_array(rg.platforms, ';'))) AS platform_name
  FROM raw_games rg
  JOIN games g ON rg.app_id = g.app_id
  WHERE rg.platforms IS NOT NULL
)
INSERT INTO game_platforms (game_id, platform_id)
SELECT t.game_id, pl.platform_id
FROM t
JOIN platforms pl ON pl.name = t.platform_name
ON CONFLICT DO NOTHING;
