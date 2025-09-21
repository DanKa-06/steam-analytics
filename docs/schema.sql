--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: developers; Type: TABLE; Schema: public; Owner: steam_user
--

CREATE TABLE public.developers (
    developer_id integer NOT NULL,
    name text
);


ALTER TABLE public.developers OWNER TO steam_user;

--
-- Name: developers_developer_id_seq; Type: SEQUENCE; Schema: public; Owner: steam_user
--

CREATE SEQUENCE public.developers_developer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.developers_developer_id_seq OWNER TO steam_user;

--
-- Name: developers_developer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: steam_user
--

ALTER SEQUENCE public.developers_developer_id_seq OWNED BY public.developers.developer_id;


--
-- Name: game_genres; Type: TABLE; Schema: public; Owner: steam_user
--

CREATE TABLE public.game_genres (
    game_id integer NOT NULL,
    genre_id integer NOT NULL
);


ALTER TABLE public.game_genres OWNER TO steam_user;

--
-- Name: game_platforms; Type: TABLE; Schema: public; Owner: steam_user
--

CREATE TABLE public.game_platforms (
    game_id integer NOT NULL,
    platform_id integer NOT NULL
);


ALTER TABLE public.game_platforms OWNER TO steam_user;

--
-- Name: games; Type: TABLE; Schema: public; Owner: steam_user
--

CREATE TABLE public.games (
    game_id integer NOT NULL,
    app_id integer,
    name text,
    release_date date,
    developer_id integer,
    publisher_id integer,
    price numeric(10,2),
    average_playtime integer,
    positive_ratings integer,
    negative_ratings integer
);


ALTER TABLE public.games OWNER TO steam_user;

--
-- Name: games_game_id_seq; Type: SEQUENCE; Schema: public; Owner: steam_user
--

CREATE SEQUENCE public.games_game_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.games_game_id_seq OWNER TO steam_user;

--
-- Name: games_game_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: steam_user
--

ALTER SEQUENCE public.games_game_id_seq OWNED BY public.games.game_id;


--
-- Name: genres; Type: TABLE; Schema: public; Owner: steam_user
--

CREATE TABLE public.genres (
    genre_id integer NOT NULL,
    name text
);


ALTER TABLE public.genres OWNER TO steam_user;

--
-- Name: genres_genre_id_seq; Type: SEQUENCE; Schema: public; Owner: steam_user
--

CREATE SEQUENCE public.genres_genre_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.genres_genre_id_seq OWNER TO steam_user;

--
-- Name: genres_genre_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: steam_user
--

ALTER SEQUENCE public.genres_genre_id_seq OWNED BY public.genres.genre_id;


--
-- Name: platforms; Type: TABLE; Schema: public; Owner: steam_user
--

CREATE TABLE public.platforms (
    platform_id integer NOT NULL,
    name text
);


ALTER TABLE public.platforms OWNER TO steam_user;

--
-- Name: platforms_platform_id_seq; Type: SEQUENCE; Schema: public; Owner: steam_user
--

CREATE SEQUENCE public.platforms_platform_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.platforms_platform_id_seq OWNER TO steam_user;

--
-- Name: platforms_platform_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: steam_user
--

ALTER SEQUENCE public.platforms_platform_id_seq OWNED BY public.platforms.platform_id;


--
-- Name: publishers; Type: TABLE; Schema: public; Owner: steam_user
--

CREATE TABLE public.publishers (
    publisher_id integer NOT NULL,
    name text
);


ALTER TABLE public.publishers OWNER TO steam_user;

--
-- Name: publishers_publisher_id_seq; Type: SEQUENCE; Schema: public; Owner: steam_user
--

CREATE SEQUENCE public.publishers_publisher_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.publishers_publisher_id_seq OWNER TO steam_user;

--
-- Name: publishers_publisher_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: steam_user
--

ALTER SEQUENCE public.publishers_publisher_id_seq OWNED BY public.publishers.publisher_id;


--
-- Name: purchases; Type: TABLE; Schema: public; Owner: steam_user
--

CREATE TABLE public.purchases (
    purchase_id integer NOT NULL,
    user_id integer,
    game_id integer,
    purchase_date timestamp without time zone,
    price numeric(10,2)
);


ALTER TABLE public.purchases OWNER TO steam_user;

--
-- Name: purchases_purchase_id_seq; Type: SEQUENCE; Schema: public; Owner: steam_user
--

CREATE SEQUENCE public.purchases_purchase_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.purchases_purchase_id_seq OWNER TO steam_user;

--
-- Name: purchases_purchase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: steam_user
--

ALTER SEQUENCE public.purchases_purchase_id_seq OWNED BY public.purchases.purchase_id;


--
-- Name: raw_games; Type: TABLE; Schema: public; Owner: steam_user
--

CREATE TABLE public.raw_games (
    app_id integer,
    name text,
    release_date date,
    english integer,
    developer text,
    publisher text,
    platforms text,
    required_age integer,
    categories text,
    genres text,
    steamspy_tags text,
    achievements integer,
    positive_ratings integer,
    negative_ratings integer,
    average_playtime integer,
    median_playtime integer,
    owners text,
    price numeric
);


ALTER TABLE public.raw_games OWNER TO steam_user;

--
-- Name: reviews; Type: TABLE; Schema: public; Owner: steam_user
--

CREATE TABLE public.reviews (
    review_id integer NOT NULL,
    user_id integer,
    game_id integer,
    rating integer,
    review_text text,
    review_date timestamp without time zone
);


ALTER TABLE public.reviews OWNER TO steam_user;

--
-- Name: reviews_review_id_seq; Type: SEQUENCE; Schema: public; Owner: steam_user
--

CREATE SEQUENCE public.reviews_review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reviews_review_id_seq OWNER TO steam_user;

--
-- Name: reviews_review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: steam_user
--

ALTER SEQUENCE public.reviews_review_id_seq OWNED BY public.reviews.review_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: steam_user
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username text,
    country text,
    registration_date date
);


ALTER TABLE public.users OWNER TO steam_user;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: steam_user
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO steam_user;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: steam_user
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: developers developer_id; Type: DEFAULT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.developers ALTER COLUMN developer_id SET DEFAULT nextval('public.developers_developer_id_seq'::regclass);


--
-- Name: games game_id; Type: DEFAULT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.games ALTER COLUMN game_id SET DEFAULT nextval('public.games_game_id_seq'::regclass);


--
-- Name: genres genre_id; Type: DEFAULT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.genres ALTER COLUMN genre_id SET DEFAULT nextval('public.genres_genre_id_seq'::regclass);


--
-- Name: platforms platform_id; Type: DEFAULT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.platforms ALTER COLUMN platform_id SET DEFAULT nextval('public.platforms_platform_id_seq'::regclass);


--
-- Name: publishers publisher_id; Type: DEFAULT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.publishers ALTER COLUMN publisher_id SET DEFAULT nextval('public.publishers_publisher_id_seq'::regclass);


--
-- Name: purchases purchase_id; Type: DEFAULT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.purchases ALTER COLUMN purchase_id SET DEFAULT nextval('public.purchases_purchase_id_seq'::regclass);


--
-- Name: reviews review_id; Type: DEFAULT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.reviews ALTER COLUMN review_id SET DEFAULT nextval('public.reviews_review_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Name: developers developers_name_key; Type: CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.developers
    ADD CONSTRAINT developers_name_key UNIQUE (name);


--
-- Name: developers developers_pkey; Type: CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.developers
    ADD CONSTRAINT developers_pkey PRIMARY KEY (developer_id);


--
-- Name: game_genres game_genres_pkey; Type: CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.game_genres
    ADD CONSTRAINT game_genres_pkey PRIMARY KEY (game_id, genre_id);


--
-- Name: game_platforms game_platforms_pkey; Type: CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.game_platforms
    ADD CONSTRAINT game_platforms_pkey PRIMARY KEY (game_id, platform_id);


--
-- Name: games games_app_id_key; Type: CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_app_id_key UNIQUE (app_id);


--
-- Name: games games_pkey; Type: CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_pkey PRIMARY KEY (game_id);


--
-- Name: genres genres_name_key; Type: CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.genres
    ADD CONSTRAINT genres_name_key UNIQUE (name);


--
-- Name: genres genres_pkey; Type: CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.genres
    ADD CONSTRAINT genres_pkey PRIMARY KEY (genre_id);


--
-- Name: platforms platforms_name_key; Type: CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.platforms
    ADD CONSTRAINT platforms_name_key UNIQUE (name);


--
-- Name: platforms platforms_pkey; Type: CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.platforms
    ADD CONSTRAINT platforms_pkey PRIMARY KEY (platform_id);


--
-- Name: publishers publishers_name_key; Type: CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.publishers
    ADD CONSTRAINT publishers_name_key UNIQUE (name);


--
-- Name: publishers publishers_pkey; Type: CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.publishers
    ADD CONSTRAINT publishers_pkey PRIMARY KEY (publisher_id);


--
-- Name: purchases purchases_pkey; Type: CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.purchases
    ADD CONSTRAINT purchases_pkey PRIMARY KEY (purchase_id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (review_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: game_genres game_genres_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.game_genres
    ADD CONSTRAINT game_genres_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(game_id);


--
-- Name: game_genres game_genres_genre_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.game_genres
    ADD CONSTRAINT game_genres_genre_id_fkey FOREIGN KEY (genre_id) REFERENCES public.genres(genre_id);


--
-- Name: game_platforms game_platforms_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.game_platforms
    ADD CONSTRAINT game_platforms_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(game_id);


--
-- Name: game_platforms game_platforms_platform_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.game_platforms
    ADD CONSTRAINT game_platforms_platform_id_fkey FOREIGN KEY (platform_id) REFERENCES public.platforms(platform_id);


--
-- Name: games games_developer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_developer_id_fkey FOREIGN KEY (developer_id) REFERENCES public.developers(developer_id);


--
-- Name: games games_publisher_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_publisher_id_fkey FOREIGN KEY (publisher_id) REFERENCES public.publishers(publisher_id);


--
-- Name: purchases purchases_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.purchases
    ADD CONSTRAINT purchases_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(game_id);


--
-- Name: purchases purchases_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.purchases
    ADD CONSTRAINT purchases_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: reviews reviews_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(game_id);


--
-- Name: reviews reviews_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: steam_user
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

