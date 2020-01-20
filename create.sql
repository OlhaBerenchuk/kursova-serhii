-- SCHEMA: public

-- DROP SCHEMA public ;

CREATE SCHEMA public
    AUTHORIZATION twewxikheafkcm;

COMMENT ON SCHEMA public
    IS 'standard public schema';

GRANT ALL ON SCHEMA public TO PUBLIC;

GRANT ALL ON SCHEMA public TO twewxikheafkcm;

-- Table: public.orm_company

-- DROP TABLE public.orm_company;

CREATE TABLE public.orm_company
(
    id integer NOT NULL DEFAULT nextval('orm_company_id_seq'::regclass),
    company_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    website character varying(100) COLLATE pg_catalog."default",
    secret_key character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT orm_company_pkey PRIMARY KEY (id),
    CONSTRAINT orm_company_company_name_key UNIQUE (company_name)

)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.orm_company
    OWNER to twewxikheafkcm;

-- Table: public.orm_project

-- DROP TABLE public.orm_project;

CREATE TABLE public.orm_project
(
    id integer NOT NULL DEFAULT nextval('orm_project_id_seq'::regclass),
    project_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    description character varying(100) COLLATE pg_catalog."default",
    company_id integer,
    CONSTRAINT orm_project_pkey PRIMARY KEY (id),
    CONSTRAINT orm_project_company_id_fkey FOREIGN KEY (company_id)
        REFERENCES public.orm_company (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.orm_project
    OWNER to twewxikheafkcm;

-- Table: public.orm_user

-- DROP TABLE public.orm_user;

CREATE TABLE public.orm_user
(
    user_email character varying(45) COLLATE pg_catalog."default" NOT NULL,
    user_username character varying(45) COLLATE pg_catalog."default" NOT NULL,
    user_password character varying(64) COLLATE pg_catalog."default" NOT NULL,
    is_owner boolean,
    company_id integer,
    CONSTRAINT orm_user_pkey PRIMARY KEY (user_username),
    CONSTRAINT orm_user_company_id_fkey FOREIGN KEY (company_id)
        REFERENCES public.orm_company (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.orm_user
    OWNER to twewxikheafkcm;

-- Table: public.orm_file

-- DROP TABLE public.orm_file;

CREATE TABLE public.orm_file
(
    id integer NOT NULL DEFAULT nextval('orm_file_id_seq'::regclass),
    file_name character varying(45) COLLATE pg_catalog."default" NOT NULL,
    upload_time character varying(100) COLLATE pg_catalog."default" NOT NULL,
    documentation character varying(45) COLLATE pg_catalog."default",
    user_username character varying(45) COLLATE pg_catalog."default",
    project_id integer,
    CONSTRAINT orm_file_pkey PRIMARY KEY (id),
    CONSTRAINT orm_file_project_id_fkey FOREIGN KEY (project_id)
        REFERENCES public.orm_project (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT orm_file_user_username_fkey FOREIGN KEY (user_username)
        REFERENCES public.orm_user (user_username) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.orm_file
    OWNER to twewxikheafkcm;