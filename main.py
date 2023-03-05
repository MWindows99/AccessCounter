import datetime
import configparser
import uvicorn
import mysql.connector
from fastapi import FastAPI, Request

config = configparser.ConfigParser()
config.read("config.ini")

Database_host = str(config.get("DATABASE", "HOST"))
Database_port = int(config.get("DATABASE", "PORT"))
Database_user = str(config.get("DATABASE", "USER"))
Database_pawd = str(config.get("DATABASE", "PASSWORD"))
Database_name = str(config.get("DATABASE", "NAME"))

app = FastAPI()

def Database(SQL, DATA, OPERATION):
    connection = mysql.connector.connect(
        host = Database_host,
        port = Database_port,
        user = Database_user,
        password = Database_pawd,
        database = Database_name
    )
    connection.autocommit = True
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(SQL, DATA)
        connection.commit()
    except:
        return False
    if OPERATION:
        return True
    else:
        if cursor.rowcount == 0:
            return None
        else:
            return cursor.fetchone()

ACCESS_COUNTS = Database("SELECT * FROM Counter", None, False)

@app.get("/count/")
async def count(request: Request):
    ipaddr = request.client.host
    if ACCESS_COUNTS == False:
        return 0
    ACCESS_COUNT = ACCESS_COUNTS[1]
    history = Database("SELECT * FROM AccessCounter WHERE IP = %s", (ipaddr,), False)
    if history is None:
        save = Database("INSERT INTO AccessCounter VALUES(%s, %s)", (ipaddr, datetime.datetime.now()), True)
        ACCESS_COUNT += 1
        result = Database("INSERT INTO Counter (COUNT) VALUES(%s)", (ACCESS_COUNT,), True)
    elif not history:
        save = False
        result = False
    else:
        now = datetime.datetime.now()
        if (now - history[1]).days >= 1:
            save = Database("UPDATE AccessCounter SET TIMESTAMP = %s  WHERE IP = %s", (now, ipaddr), True)
            ACCESS_COUNT += 1
            result = Database("INSERT INTO Counter (COUNT) VALUES(%s)", (ACCESS_COUNT,), True)
        else:
            save = True
            result = True
    if not save or not result:
        return 0
    return ACCESS_COUNT

# Run Application
uvicorn.run(app, host="0.0.0.0", port=8800)
