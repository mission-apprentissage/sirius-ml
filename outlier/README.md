# SIRIUS-OUTLIER

## 0. Add environment variable
The application depends on this secret environment variables:
- $SIRIUS_HF_TOKEN
- $SIRIUS_MISTRAL_API_KEY

## 1. Test application

### Install the requirements

`cd sirius-outlier && python3 -m venv .venv && source .venv/bin/activate`

`pip install -r requirements.txt`

### Start the application
`fastapi dev app/api.py`

### Test endpoints

#### Scoring
`curl 'http://127.0.0.1:8000/score' -X POST -H 'Content-Type: application/json' -d '{"id": "test"} --data-binary ./dataset/temoignages.csv`

#### Detection
`curl 'http://127.0.0.1:8000/detect' -X POST -H 'Content-Type: application/json' -d '{"scores":[-9.890680333249605,-8.81517297694887,-10.817086031345966,-9.134718245421285,-9.136104401859312,-10.10892008829345,-9.246591666943132], "percent": 1}'`

## 2. Create image

### Build image
`docker buildx build -t sirius-outlier .`

### Run image
`docker run -p 8000:8000 --name outlier -e SIRIUS_HF_TOKEN="$SIRIUS_HF_TOKEN" -e SIRIUS_MISTRAL_API_KEY="$SIRIUS_MISTRAL_API_KEY" sirius-outlier`


### Test endpoints
`curl 'http://0.0.0.0:8000/score' -X POST -H 'Content-Type: application/json' -d '{"text": "patisserie ou cuisine"}'`

`curl 'http://0.0.0.0:8000/expose' -X POST -H 'Content-Type: application/json' -d '{"text": "Il faut se lever tôt le matin et tenir toute la journée mais ça vaut le coup! Surtout si tu es en fauteuil roulant"}'`


### Stop and remove image
`docker stop outlier && docker rm outlier`


## 3. Deploy on OVHcloud
[TODO]