from fastapi import FastAPI
from typing import Dict
from anonymizer import Anonymizer

app = FastAPI()

# Instanciate anonymiser
anonymizer = Anonymizer()

@app.get("/") 
def root():
    print('[sirius-anonymization] Request for index page received.')
    return {"status": "sirius-anonymization API running."}

@app.post("/anonymize")
def anonymize(query: Dict):
    text = query['text']
    print(f"[sirius-anonymization] Anonymizing: '{text}'...")

    # Anonymizing text
    anonymization = anonymizer.anonymize(text)
    print(f"[sirius-anonymization] Anonymized: {anonymization}")

    return anonymization