-- SEQUENCE: public.orm_company_id_seq

-- DROP SEQUENCE public.orm_company_id_seq;

CREATE SEQUENCE public.orm_company_id_seq
    INCREMENT 1
    START 4
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.orm_company_id_seq
    OWNER TO twewxikheafkcm;

-- SEQUENCE: public.orm_project_id_seq

-- DROP SEQUENCE public.orm_project_id_seq;

CREATE SEQUENCE public.orm_project_id_seq
    INCREMENT 1
    START 5
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.orm_project_id_seq
    OWNER TO twewxikheafkcm;

-- SEQUENCE: public.orm_file_id_seq

-- DROP SEQUENCE public.orm_file_id_seq;

CREATE SEQUENCE public.orm_file_id_seq
    INCREMENT 1
    START 7
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.orm_file_id_seq
    OWNER TO twewxikheafkcm;

-- Constraint: orm_company_company_name_key

-- ALTER TABLE public.orm_company DROP CONSTRAINT orm_company_company_name_key;

ALTER TABLE public.orm_company
    ADD CONSTRAINT orm_company_company_name_key UNIQUE (company_name);

-- Constraint: orm_company_pkey

-- ALTER TABLE public.orm_company DROP CONSTRAINT orm_company_pkey;

ALTER TABLE public.orm_company
    ADD CONSTRAINT orm_company_pkey PRIMARY KEY (id);

-- Constraint: orm_project_company_id_fkey

-- ALTER TABLE public.orm_project DROP CONSTRAINT orm_project_company_id_fkey;

ALTER TABLE public.orm_project
    ADD CONSTRAINT orm_project_company_id_fkey FOREIGN KEY (company_id)
    REFERENCES public.orm_company (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

-- Constraint: orm_project_pkey

-- ALTER TABLE public.orm_project DROP CONSTRAINT orm_project_pkey;

ALTER TABLE public.orm_project
    ADD CONSTRAINT orm_project_pkey PRIMARY KEY (id);

-- Constraint: orm_user_company_id_fkey

-- ALTER TABLE public.orm_user DROP CONSTRAINT orm_user_company_id_fkey;

ALTER TABLE public.orm_user
    ADD CONSTRAINT orm_user_company_id_fkey FOREIGN KEY (company_id)
    REFERENCES public.orm_company (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

-- Constraint: orm_user_pkey

-- ALTER TABLE public.orm_user DROP CONSTRAINT orm_user_pkey;

ALTER TABLE public.orm_user
    ADD CONSTRAINT orm_user_pkey PRIMARY KEY (user_username);

-- Constraint: orm_file_pkey

-- ALTER TABLE public.orm_file DROP CONSTRAINT orm_file_pkey;

ALTER TABLE public.orm_file
    ADD CONSTRAINT orm_file_pkey PRIMARY KEY (id);

-- Constraint: orm_file_project_id_fkey

-- ALTER TABLE public.orm_file DROP CONSTRAINT orm_file_project_id_fkey;

ALTER TABLE public.orm_file
    ADD CONSTRAINT orm_file_project_id_fkey FOREIGN KEY (project_id)
    REFERENCES public.orm_project (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

-- Constraint: orm_file_user_username_fkey

-- ALTER TABLE public.orm_file DROP CONSTRAINT orm_file_user_username_fkey;

ALTER TABLE public.orm_file
    ADD CONSTRAINT orm_file_user_username_fkey FOREIGN KEY (user_username)
    REFERENCES public.orm_user (user_username) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
