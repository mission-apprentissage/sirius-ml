from fastapi import FastAPI, Request
from typing import Dict
from app.outlier import Outlier, create_dataset
import numpy as np

app = FastAPI()

# Instanciate classifier models
clf = Outlier()

@app.get("/")
async def root():
    print('[sirius-outlier] Request for index page received')
    return {"status": "sirius-outlier API running."}

@app.post("/score")
async def score(request: Request):
    print('[score] Receive request', request)

    # Load datas
    form = await request.form()
    bytes_data = await form["file"].read()
    # file_id = form['id']

    # Create dataset
    dataset = create_dataset(bytes_data)

    # Scoring dataset
    scores = clf.fit(dataset)

    return {'scores': scores}

@app.post("/detect")
def detect(query: Dict):
    # Get the score for each sample
    scores = query['scores']
    print(f"Loaded {len(scores)} scores.")

    # Get the score threshold for anomaly
    percent = query['percent']
    threshold = np.percentile(scores, percent)
    print(f"{percent}% threshold score: {threshold:.4f}")

    # Label the outliers
    outliers = [int(x < threshold) for x in scores]
    print(f"Detected {sum(outliers)} outliers.")
    return {'threshold': threshold, 'outliers': outliers}