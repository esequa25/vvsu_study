
CREATE TABLE IF NOT EXISTS public.users
(
    id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    username text COLLATE pg_catalog."default" NOT NULL,
    email text COLLATE pg_catalog."default",
    creation_date date,
    CONSTRAINT users_pkey PRIMARY KEY (id)
)


CREATE TABLE IF NOT EXISTS public.topics
(
    id integer NOT NULL DEFAULT nextval('topics_id_seq'::regclass),
    user_id bigint,
    title text COLLATE pg_catalog."default" NOT NULL,
    content text COLLATE pg_catalog."default",
    creation_date date,
    CONSTRAINT topics_pkey PRIMARY KEY (id),
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)


CREATE TABLE IF NOT EXISTS public.comments
(
    id integer NOT NULL DEFAULT nextval('comments_id_seq'::regclass),
    topic_id bigint,
    user_id bigint,
    content text COLLATE pg_catalog."default" NOT NULL,
    creation_date date,
    is_anon boolean NOT NULL,
    CONSTRAINT comments_pkey PRIMARY KEY (id),
    CONSTRAINT topic_id FOREIGN KEY (topic_id)
        REFERENCES public.topics (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)


CREATE TABLE IF NOT EXISTS public.logs
(
    id integer NOT NULL DEFAULT nextval('logs_id_seq'::regclass),
    user_id bigint,
    action_type text COLLATE pg_catalog."default",
    action_id bigint,
    server_response text COLLATE pg_catalog."default",
    creation_date date,
    description text COLLATE pg_catalog."default",
    CONSTRAINT logs_pkey PRIMARY KEY (id)
)
