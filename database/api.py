from fastapi import FastAPI
from typing import Dict
from database import DB
import os
from ipwhois import IPWhois
from requests import get

app = FastAPI()

# Instanciate database
db = DB(db=os.environ['SIRIUS_DB_URL'])

# Get IP adress for database connection
ip = get('https://api.ipify.org').text
whois = IPWhois(ip).lookup_rdap(depth=1)
cidr = whois['network']['cidr']
name = whois['network']['name']
print('Provider:  ', name)
print('Public IP: ', ip)
print('CIDRs:     ', cidr)

@app.get("/")
def root():
    print('[sirius-database] Request for index page received.')
    return {"status": "sirius-database API running."}

@app.post("/load")
def load(query: Dict):
    table = query['table']
    print(f'[sirius-database] Loading SIRIUS {table} database...')

    # Load database
    return db.load(table=table)