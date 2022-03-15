
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PWD = os.getenv("DB_PASSWORD")

def init_db():

    conn = psycopg2.connect(f"dbname='postgres' user='{DB_USERNAME}' host='{DB_HOST}' password='{DB_PWD}'")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("""
    select exists(
        SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('persons')
        );""")
        
    exists = next(iter(cur), False)[0]
    
    if not exists:
    
        cur.execute("""
        CREATE DATABASE persons
            WITH 
            OWNER = postgres
            ENCODING = 'UTF8'
            TABLESPACE = pg_default
            CONNECTION LIMIT = -1;
        """)

        cur.execute("GRANT ALL ON DATABASE persons TO postgres;")
        cur.execute(f"GRANT ALL ON DATABASE persons TO {DB_USERNAME}")
        cur.execute("GRANT TEMPORARY, CONNECT ON DATABASE persons TO PUBLIC;")


        conn = psycopg2.connect(f"dbname='persons' user='{DB_USERNAME}' host='{DB_HOST}' password='{DB_PWD}'")
        cur = conn.cursor()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
        conn.autocommit = True

        cur.execute("""
        CREATE TABLE person (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                last_name VARCHAR NOT NULL,
                company_name VARCHAR NOT NULL
            );
        """)
        
        cur.execute("""
        insert into public.person (id, first_name, last_name, company_name) values (5, 'Taco', 'Fargo', 'Alpha Omega Upholstery');
        insert into public.person (id, first_name, last_name, company_name) values (6, 'Frank', 'Shader', 'USDA');
        insert into public.person (id, first_name, last_name, company_name) values (1, 'Pam', 'Trexler', 'Hampton, Hampton and McQuill');
        insert into public.person (id, first_name, last_name, company_name) values (8, 'Paul', 'Badman', 'Paul Badman & Associates');
        insert into public.person (id, first_name, last_name, company_name) values (9, 'Otto', 'Spring', 'The Chicken Sisters Restaurant');
        """)

