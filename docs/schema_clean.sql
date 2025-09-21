CREATE TABLE developers (
    developer_id int PRIMARY KEY,
    name text UNIQUE
);

CREATE TABLE publishers (
    publisher_id int PRIMARY KEY,
    name text UNIQUE
);

CREATE TABLE games (
    game_id int PRIMARY KEY,
    app_id int UNIQUE,
    name text,
    release_date date,
    developer_id int,
    publisher_id int,
    price numeric,
    average_playtime int,
    positive_ratings int,
    negative_ratings int,
    FOREIGN KEY (developer_id) REFERENCES developers(developer_id),
    FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id)
);

CREATE TABLE genres (
    genre_id int PRIMARY KEY,
    name text UNIQUE
);

CREATE TABLE platforms (
    platform_id int PRIMARY KEY,
    name text UNIQUE
);

CREATE TABLE game_genres (
    game_id int,
    genre_id int,
    PRIMARY KEY (game_id, genre_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);

CREATE TABLE game_platforms (
    game_id int,
    platform_id int,
    PRIMARY KEY (game_id, platform_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (platform_id) REFERENCES platforms(platform_id)
);

CREATE TABLE users (
    user_id int PRIMARY KEY,
    username text,
    country text,
    registration_date date
);

CREATE TABLE purchases (
    purchase_id int PRIMARY KEY,
    user_id int,
    game_id int,
    purchase_date timestamp,
    price numeric,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id)
);

CREATE TABLE reviews (
    review_id int PRIMARY KEY,
    user_id int,
    game_id int,
    rating int,
    review_text text,
    review_date timestamp,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id)
);

-- staging table (not linked to others)
CREATE TABLE raw_games (
    app_id int,
    name text,
    release_date date,
    english int,
    developer text,
    publisher text,
    platforms text,
    required_age int,
    categories text,
    genres text,
    steamspy_tags text,
    achievements int,
    positive_ratings int,
    negative_ratings int,
    average_playtime int,
    median_playtime int,
    owners text,
    price numeric
);
