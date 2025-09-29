--Select top 10 games
SELECT * FROM games LIMIT 10;

--Filter + ORDER BY: games released after 2018, order by positive_ratings desc
SELECT name, release_date, positive_ratings FROM games
WHERE release_date >= '2018-01-01'
ORDER BY positive_ratings DESC
LIMIT 20;

-- Count games per developer (top 10)
SELECT d.name AS developer, COUNT(g.game_id) AS games_count
FROM games g
JOIN developers d ON g.developer_id = d.developer_id
GROUP BY d.name
ORDER BY games_count DESC
LIMIT 10;

-- top 10 games by purchases
SELECT g.name, COUNT(p.purchase_id) AS purchases_count
FROM purchases p
JOIN games g ON p.game_id = g.game_id
GROUP BY g.name
ORDER BY purchases_count DESC
LIMIT 10;

-- 10 Analytical topics (SQL queries)

-- Top 10 best-selling games by number of purchases
SELECT g.name, COUNT(p.purchase_id) AS sales
FROM purchases p
JOIN games g ON p.game_id = g.game_id
GROUP BY g.name
ORDER BY sales DESC
LIMIT 10;

-- Revenue by year
SELECT DATE_TRUNC('year', purchase_date) AS year, SUM(price) AS total_revenue
FROM purchases
GROUP BY year
ORDER BY year;

-- Average price by platform
SELECT pl.name AS platform, AVG(p.price) AS avg_price
FROM purchases p
JOIN game_platforms gp ON p.game_id = gp.game_id
JOIN platforms pl ON gp.platform_id = pl.platform_id
GROUP BY pl.name
ORDER BY avg_price DESC;

-- Average playtime by genre
SELECT ge.name AS genre, AVG(g.average_playtime) AS avg_playtime
FROM game_genres gg
JOIN genres ge ON gg.genre_id = ge.genre_id
JOIN games g ON gg.game_id = g.game_id
GROUP BY ge.name
ORDER BY avg_playtime DESC;

-- Top developers by total revenue
SELECT d.name AS developer, SUM(p.price) AS revenue
FROM purchases p
JOIN games g ON p.game_id = g.game_id
JOIN developers d ON g.developer_id = d.developer_id
GROUP BY d.name
ORDER BY revenue DESC
LIMIT 10;

-- Purchase distribution by country (top 10 countries)
SELECT u.country, COUNT(p.purchase_id) AS purchases
FROM purchases p
JOIN users u ON p.user_id = u.user_id
GROUP BY u.country
ORDER BY purchases DESC
LIMIT 10;

-- Rating distribution by genre (average rating) -- requires reviews table
SELECT ge.name AS genre, AVG(r.rating) AS avg_rating
FROM reviews r
JOIN games g ON r.game_id = g.game_id
JOIN game_genres gg ON gg.game_id = g.game_id
JOIN genres ge ON gg.genre_id = ge.genre_id
GROUP BY ge.name
ORDER BY avg_rating DESC
LIMIT 10;

-- Games with highest positive/negative rating ratio
SELECT name, positive_ratings, negative_ratings,
  CASE WHEN negative_ratings = 0 THEN positive_ratings ELSE (positive_ratings::float / negative_ratings) END AS pos_neg_ratio
FROM games
WHERE positive_ratings IS NOT NULL
ORDER BY pos_neg_ratio DESC
LIMIT 15;

-- Daily purchases trend for last 30 days
SELECT DATE(purchase_date) AS day, COUNT(*) AS purchases
FROM purchases
WHERE purchase_date >= (CURRENT_DATE - INTERVAL '30 days')
GROUP BY day
ORDER BY day;

-- Price buckets vs average playtime
SELECT width_bucket(g.price, 0, 60, 6) AS price_bucket,
       MIN(g.price) AS min_price, MAX(g.price) AS max_price,
       AVG(g.average_playtime) AS avg_playtime,
       COUNT(*) AS games_count
FROM games g
GROUP BY price_bucket
ORDER BY price_bucket;
