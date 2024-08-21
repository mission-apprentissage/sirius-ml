# SIRIUS-API

## 0. Add environment variable
The application depends on this secret environment variables:
- SIRIUS_HF_TOKEN
- SIRIUS_MISTRAL_API_KEY

## 1. Test application

### Install the requirements

`cd sirius-moderation && python3 -m venv .venv && source .venv/bin/activate`

`pip install -r requirements.txt`

### Start the application
`fastapi dev app/api.py`

or `uvicorn app.api:app --reload`

or `gunicorn app.api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker`

### Example call
http://127.0.0.1:8000/


## 2. Create image

### Build image
`docker buildx -t sirius-moderation .`

### Run image
`docker run -d --name moderation -p 0.0.0.0:8000 sirius-moderation`

### Stop and remove image
`docker stop moderation && docker rm moderation`


## 3. Deploy on OVHcloud
[TODO]