-- Table: public.user
-- To store username, name, and hashed password
-- DROP TABLE IF EXISTS public."user";

CREATE TABLE IF NOT EXISTS public."user"
(
    id integer NOT NULL DEFAULT nextval('user_id_seq'::regclass),
    username text COLLATE pg_catalog."default",
    password text COLLATE pg_catalog."default",
    name text COLLATE pg_catalog."default",
    CONSTRAINT user_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."user"
    OWNER to postgres;

-----------------------------------------------------------------------------------
-- Table: public.blackList
-- To store blacklisted url, that is associated with the user id from user table
-- DROP TABLE IF EXISTS public."blackList";

CREATE TABLE IF NOT EXISTS public."blackList"
(
    id integer NOT NULL DEFAULT nextval('"Blacklist_id_seq"'::regclass),
    user_id integer,
    blacklisted_url text COLLATE pg_catalog."default",
    CONSTRAINT "Blacklist_pkey" PRIMARY KEY (id),
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES public."user" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."blackList"
    OWNER to postgres;

---------------------------------------------------------------------------------
-- Table: public.whiteList
-- To store whitelisted url, that is associated with the user id from user table
-- DROP TABLE IF EXISTS public."whiteList";

CREATE TABLE IF NOT EXISTS public."whiteList"
(
    id integer NOT NULL DEFAULT nextval('"whiteList_id_seq"'::regclass),
    user_id integer,
    whitelisted_url text COLLATE pg_catalog."default",
    CONSTRAINT "whiteList_pkey" PRIMARY KEY (id),
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES public."user" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."whiteList"
    OWNER to postgres;

-----------------------------------------------------------------------------------
-- Table: public.phishingAttempts
-- To store the phishing attacks
-- Store timestamps, the url, and the decision tree prediction
-- DROP TABLE IF EXISTS public."phishingAttempts";

CREATE TABLE IF NOT EXISTS public."phishingAttempts"
(
    id integer NOT NULL DEFAULT nextval('"phishingAttempts_id_seq"'::regclass),
    "timestamp" timestamp with time zone,
    phishing_url text COLLATE pg_catalog."default",
    decision_tree_prediction boolean,
    user_id integer,
    CONSTRAINT "phishingAttempts_pkey" PRIMARY KEY (id),
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES public."user" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."phishingAttempts"
    OWNER to postgres;
