
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
        SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('locations')
        );""")
    
    exists, = next(iter(cur), (False,))
    print(f"Init db?: {str(exists)}")

    if not exists:

        print("Init db ...")
        cur.execute("""
        CREATE DATABASE locations
            WITH 
            OWNER = postgres
            ENCODING = 'UTF8'
            TABLESPACE = pg_default
            CONNECTION LIMIT = -1;
        """)

        cur.execute("GRANT ALL ON DATABASE locations TO postgres;")
        cur.execute(f"GRANT ALL ON DATABASE locations TO {DB_USERNAME}")
        cur.execute("GRANT TEMPORARY, CONNECT ON DATABASE locations TO PUBLIC;")


        conn = psycopg2.connect(f"dbname='locations' user='{DB_USERNAME}' host='{DB_HOST}' password='{DB_PWD}'")
        cur = conn.cursor()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
        conn.autocommit = True

        cur.execute("CREATE EXTENSION postgis;")

        cur.execute("""
        CREATE TABLE location (
            id SERIAL PRIMARY KEY,
            person_id INT NOT NULL,
            coordinate GEOMETRY NOT NULL,
            creation_time TIMESTAMP NOT NULL DEFAULT NOW()
        );
        CREATE INDEX coordinate_idx ON location (coordinate);
        CREATE INDEX creation_time_idx ON location (creation_time);
        
        """)

        cur.execute("""
        insert into public.location (id, person_id, coordinate, creation_time) values (29, 1, '010100000000ADF9F197925EC0FDA19927D7C64240', '2020-08-18 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (30, 5, '010100000097FDBAD39D925EC0D00A0C59DDC64240', '2020-08-15 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (31, 5, '010100000000ADF9F197925EC0FDA19927D7C64240', '2020-08-15 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (32, 1, '0101000000477364E597925EC0FDA19927D7C64240', '2020-08-15 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (33, 1, '0101000000477364E597925EC021787C7BD7C64240', '2020-08-19 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (34, 6, '010100000097FDBAD39D925EC0D00A0C59DDC64240', '2020-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (36, 1, '010100000097FDBAD39D925EC0D00A0C59DDC64240', '2020-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (37, 1, '010100000097FDBAD39D925EC0D00A0C59DDC64240', '2020-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (38, 1, '010100000097FDBAD39D925EC0D00A0C59DDC64240', '2020-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (39, 1, '010100000097FDBAD39D925EC0D00A0C59DDC64240', '2020-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (40, 1, '010100000097FDBAD39D925EC0D00A0C59DDC64240', '2020-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (41, 1, '010100000097FDBAD39D925EC0D00A0C59DDC64240', '2020-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (42, 6, '0101000000842FA75F7D874140CEEEDAEF9AA45AC0', '2020-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (43, 6, '0101000000842FA75F7D874140CEEEDAEF9AA45AC0', '2020-07-06 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (44, 6, '0101000000842FA75F7D874140CEEEDAEF9AA45AC0', '2020-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (45, 6, '0101000000554FE61F7D87414002D9EBDD9FA45AC0', '2020-07-05 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (46, 6, '0101000000895C70067F874140CDB1BCAB9EA45AC0', '2020-04-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (47, 6, '0101000000895C70067F874140971128AC9EA45AC0', '2020-05-01 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (48, 6, '0101000000895C70067F874140CDB1BCAB9EA45AC0', '2020-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (49, 8, '0101000000895C70067F874140CDB1BCAB9EA45AC0', '2020-07-07 10:38:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (50, 8, '0101000000895C70067F874140971128AC9EA45AC0', '2020-07-07 10:38:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (51, 8, '0101000000895C70067F874140971128AC9EA45AC0', '2020-07-01 10:38:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (52, 9, '0101000000895C70067F874140971128AC9EA45AC0', '2020-07-01 10:38:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (53, 9, '0101000000842FA75F7D874140CEEEDAEF9AA45AC0', '2020-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (54, 9, '0101000000842FA75F7D874140CEEEDAEF9AA45AC0', '2019-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (55, 5, '0101000000842FA75F7D874140CEEEDAEF9A645AC0', '2019-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (56, 5, '0101000000842FA75F7D074140CEEEDAEF9A645AC0', '2019-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (57, 5, '010100000097FDBAD39D925EC0D00A0C59DDC64240', '2020-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (58, 8, '0101000000842FA75F7D874140CEEEDAEF9AA45AC0', '2020-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (59, 8, '0101000000842FA75F7D874140CEEEDAEF9AA45AC0', '2020-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (60, 8, '0101000000842FA75F7D874140CEEEDAEF9AA45AC0', '2020-07-06 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (61, 8, '0101000000842FA75F7D874140DA0FC2ED9AA45AC0', '2020-07-05 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (62, 8, '0101000000842FA75F7D8741403A18FBDC9AA45AC0', '2020-01-05 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (63, 5, '0101000000842FA75F7D8741403A18FBDC9AA45AC0', '2020-01-05 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (64, 6, '0101000000842FA75F7D8741403A18FBDC9AA45AC0', '2020-01-05 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (65, 9, '010100000097FDBAD39D925EC0D00A0C59DDC64240', '2020-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (66, 5, '010100000097FDBAD39D925EC0D00A0C59DDC64240', '2020-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (67, 8, '010100000097FDBAD39D925EC0D00A0C59DDC64240', '2020-07-07 10:37:06.000000');
        insert into public.location (id, person_id, coordinate, creation_time) values (68, 6, '010100000097FDBAD39D925EC0D00A0C59DDC64240', '2020-08-15 10:37:06.000000');

        """)
