from fastapi import FastAPI
from typing import Dict
from moderation import Classifier, expose_function
from dataset import Datas
import os
from ipwhois import IPWhois
from requests import get

app = FastAPI()

# Instanciate dataset
datas = Datas(db=os.environ['SIRIUS_DB_URL'], hf=os.environ['SIRIUS_HF_TOKEN'])

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
    repo = query['repo']
    print(f'[sirius-moderation] Updating SIRIUS {table} dataset...')

    # Extract dataset from table
    datas.read(table=table)
    datas.prepare()
    datas.encode(text_col='text')

    # Export dataset
    datas.save(repo=repo)

    return {"status": f"SIRIUS {table} dataset updated to {repo}."}

@app.post("/load")
async def load(query: Dict):
    table = query['table']
    repo = query['repo']
    print(f'[sirius-moderation] Loading SIRIUS {table} dataset...')

    # Load dataset
    datas.load(table=table, repo=repo)
    return {"status": f"SIRIUS {table} dataset loaded from {repo}."}

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