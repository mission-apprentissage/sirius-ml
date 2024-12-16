from fastapi import FastAPI
from typing import Dict
from exposition import expose_function, correct_function, anonymize_function
app = FastAPI()

@app.get("/") 
def root():
    print('[sirius-exposition] Request for index page received.')
    return {"status": "sirius-exposition API running."}

@app.post("/expose")
def expose(query: Dict):
    text = query['text']
    
    try:
        correct_prompt = query['correction']
    except:
        correct_prompt = ''

    try:
        anonymize_prompt = query['anonymization']
    except:
        anonymize_prompt = ''

    print(f"[sirius-expose] Processing text: '{text}'")

    # Exposition classifier
    print(f"1. Classifying with EXPOSITION categories:")
    exposition = expose_function(text)
    print(exposition)

    # Correction tools
    print(f"2. Correcting with prompt: {correct_prompt}")
    correction = correct_function(text, correct_prompt)
    print(correction)

    # Anonymize tools
    print(f"3. Anonymize with prompt: {anonymize_prompt}")
    anonymization = anonymize_function(correction['correction'], anonymize_prompt)
    print(anonymization)

    return {
            'text': text,
            'exposition': exposition,
            'correction': correction,
            'anonymisation': anonymization
    }