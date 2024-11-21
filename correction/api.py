from fastapi import FastAPI
from typing import Dict
from correction import Corrector

app = FastAPI()

# Instanciate corrector
corrector = Corrector()

@app.get("/") 
def root():
    print('[sirius-correction] Request for index page received.')
    return {"status": "sirius-correction API running."}

@app.post("/correct")
def correct(query: Dict):
    text = query['text']
    print(f"[sirius-correction] Correcting: '{text}'...")

    # Correcting text
    correction = corrector.correct(text)
    print(f"[sirius-correction] Correction: {correction}")

    return correction
