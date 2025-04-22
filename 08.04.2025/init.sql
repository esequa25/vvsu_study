
CREATE TABLE IF NOT EXISTS users
(
    id SERIAL PRIMARY KEY,
    username text COLLATE pg_catalog."default" NOT NULL,
    email text COLLATE pg_catalog."default",
    creation_date date
);


CREATE TABLE IF NOT EXISTS topics
(
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    title text COLLATE pg_catalog."default" NOT NULL,
    content text COLLATE pg_catalog."default",
    creation_date date,
    FOREIGN KEY (user_id) REFERENCES users (id)
);


CREATE TABLE IF NOT EXISTS comments
(
    id SERIAL PRIMARY KEY,
    topic_id INTEGER,
    user_id INTEGER,
    content text COLLATE pg_catalog."default" NOT NULL,
    creation_date date,
    is_anon boolean NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (topic_id) REFERENCES topics (id)
);


CREATE TABLE IF NOT EXISTS logs
(
    id SERIAL PRIMARY KEY,
    user_id bigint,
    action_type text COLLATE pg_catalog."default",
    action_id bigint,
    server_response text COLLATE pg_catalog."default",
    creation_date date,
    description text COLLATE pg_catalog."default",
    FOREIGN KEY (user_id) REFERENCES users (id)
);
