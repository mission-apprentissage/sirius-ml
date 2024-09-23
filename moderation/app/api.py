from fastapi import FastAPI
from typing import Dict
from app.moderation import Classifier, expose_function
from app.dataset import Dataset
import os
from ipwhois import IPWhois
from requests import get

app = FastAPI()

# Instanciate dataset
dataset = Dataset(db=os.environ['SIRIUS_DB_URL'])

# Instanciate classifier model
clf = Classifier()

# Get IP adress for database connection
ip = get('https://api.ipify.org').text
whois = IPWhois(ip).lookup_rdap(depth=1)
cidr = whois['network']['cidr']
name = whois['network']['name']
print('Provider:  ', name)
print('Public IP: ', ip)
print('CIDRs:     ', cidr)

@app.get("/")
async def root():
    print('[sirius-moderation] Request for index page received.')
    return {"status": "sirius-moderation API running."}

@app.post("/update")
async def update(query: Dict):
    table = query['table']
    print(f'[sirius-moderation] Updating SIRIUS {table} dataset...')

    # Extract dataset from table
    dataset.read(table=table)
    dataset.prepare()
    dataset.encode(text_col='text')

    # Export dataset
    dataset.save(filepath='./dataset/' + f'{table}.csv')

    return {"status": f"SIRIUS {table} dataset updated."}

@app.post("/score")
async def score(query: Dict):
    if 'rules' in query.keys():
        rules = query['rules']
    else:
        rules = ''
    text = query['text']
    models = {
        'valid' : ('NOT_VALIDATED', 'VALIDATED'),
        'unvalid': ('REJECTED', 'TO_FIX', 'ALERT'),
        # 'gem': ('NOT_GEM', 'GEM')
    }

    # Scoring text
    scores = {}
    for model, labels in models.items():
        print(f"Scoring '{text}' with '{model}' model...")
        score = clf.score(text, model)
        print(f"Probas: {score}")
        for i in range(len(labels)):
            scores[labels[i]] = score[i]

    # GEM classifier
    print(f"Classifying '{text}' with GEM rules:\n'{rules}'...")
    scores['GEM'] = clf.gem_classifier(rules, text)
    print(scores)

    return {
            'text': text,
            'scores': scores,
    }

@app.post("/expose")
async def expose(query: Dict):
    text = query['text']

    # Exposition classifier
    print(f"Classifying '{text}' with EXPOSITION categories...:")
    exposition = expose_function(text)
    print(exposition)

    return {
            'text': text,
            'exposition' : exposition,
    }
