import os
import sys
import json
import uuid
import psycopg2
import datetime
from dotenv import load_dotenv
from psycopg2.extras import execute_values

def _connection():
    # load .env file
    load_dotenv()
    dbconf = {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "pass": os.getenv("DB_PASS"),
        "name": os.getenv("DB_NAME"),
        "port": os.getenv("DB_PORT"),
    }

    # connection to database
    try:
        conn = psycopg2.connect(
            host=dbconf.get("host"),
            user=dbconf.get("user"),
            password=dbconf.get("pass"),
            dbname=dbconf.get("name"),
            port=dbconf.get("port")
        )
        print("Database ready to use!")
        return conn
    except Exception as e:
        print("Error connecting to PostgreSQL:", e)
        return None

def _read_files(t: str):
    # read json files based on type input
    filesource = None
    if t ==  "province":
        filesource = "meta_datas/provinces.json"
    elif t == "city":
        filesource = "meta_datas/cities.json"
    elif t == "district":
        filesource = "meta_datas/districts.json"
    elif t == "subdistrict":
        filesource = "meta_datas/subdistricts.json"

    with open(filesource, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    if data is not None:
        _insert(t, data)
    else:
        print("No data will executed!")

def _insert(t: str, data):
    print(f"executing data {t} with total data: {len(data)}")
    
    try:
        # prepare the data
        # convert into tuple for better performance
        dt = datetime.datetime.now()
        query = None
        values = None

        # validate {query} and {values} based on type inputted
        if t == "province":
            query = "INSERT INTO provinces (id,code,name,created_date) VALUES %s"
            values = [(
                str(uuid.uuid4()),
                v.get("id_province"),
                v.get("name_province"),
                dt
            ) for v in data]
        elif t == "city":
            query = "INSERT INTO cities (id,province_code,code,name,created_date) VALUES %s"
            values = [(
                str(uuid.uuid4()),
                v.get("id_province"),
                v.get("id_city"),
                v.get("name_city"),
                dt
            ) for v in data]
        elif t == "district":
            query = "INSERT INTO districts (id,city_code,code,name,created_date) VALUES %s"
            values = [(
                str(uuid.uuid4()),
                v.get("id_city"),
                v.get("id_district"),
                v.get("name_district"),
                dt
            ) for v in data]
        elif t == "subdistrict":
            query = "INSERT INTO subdistricts (id,district_code,code,name,created_date) VALUES %s"
            values = [(
                str(uuid.uuid4()),
                v.get("id_district"),
                v.get("id_subdistrict"),
                v.get("name_subdistrict"),
                dt
            ) for v in data]

        # perform to insert data
        conn = _connection()
        with conn.cursor() as c:
            execute_values(c, query, values)
            conn.commit()
        print(f"Data {t} is sucessfully migrated!")
    except Exception as e:
        print("Error when inserting data", e)
    finally:
        conn.close()

if __name__ == "__main__":
    # get arguments
    # t = type
    allowed_arguments = ["province", "city", "district", "subdistrict"]
    if len(sys.argv) > 1:
        t = sys.argv[1]
        if t not in allowed_arguments:
            print("Type you input is not allowed", allowed_arguments)
        else:
            _read_files(t.lower())
    else:
        print("You are not choose any type to migrate")