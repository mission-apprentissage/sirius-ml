# SIRIUS-API

## Run application

### Install the requirements
`python3 -m venv .venv && source .venv/bin/activate`

`pip install -r requirements.txt`

### Start the application
`fastapi dev app/main.py`

or `uvicorn app.main:app --reload`

or `gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker`


### Example call
http://127.0.0.1:8000/



## Create image

### Build image
`docker buildx -t sirius-api .`

### Run image
`docker run -d --name sirius -p 0.0.0.0:8000 sirius-api`

### Stop and remove image
`docker stop sirius && docker rm sirius`
