from fastapi import FastAPI
from typing import Dict
from app.moderation import Classifier, expose_function

app = FastAPI()

# Instanciate classifier models
clf = Classifier()

@app.get("/")
async def root():
    print('[sirius-moderation] Request for index page received')
    return {"status": "sirius-moderation API running."}

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
