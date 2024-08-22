# SIRIUS-MODERATION

## 0. Add environment variable
The application depends on this secret environment variables:
- $SIRIUS_HF_TOKEN
- $SIRIUS_MISTRAL_API_KEY

## 1. Test application

### Install the requirements

`cd moderation && python3 -m venv .venv && source .venv/bin/activate`

`pip install -r requirements.txt`

### Start the application
`fastapi dev app/api.py`

### Test endpoints

#### Short text
`curl 'http://127.0.0.1:8000/score' -X POST -H 'Content-Type: application/json' -d '{"text": "patisserie ou cuisine"}'`

#### With rules
`curl 'http://127.0.0.1:8000/score' -X POST -H 'Content-Type: application/json' -d '{"text": "tkt, ça va le faire si tu supportes l’OM !", "rules": "\n- Il suffit de supporter l’OM\n"}'`

#### Exposition
`curl 'http://127.0.0.1:8000/expose' -X POST -H 'Content-Type: application/json' -d '{"text": "Il faut se lever tôt le matin et tenir toute la journée mais ça vaut le coup! Surtout si tu es en fauteuil roulant"}'`


## 2. Create image

### Build image
`docker buildx build --platform linux/amd64 -t sirius-moderation .`

### Run image
`docker run -p 8000:8000 --name moderation -e SIRIUS_HF_TOKEN="$SIRIUS_HF_TOKEN" -e SIRIUS_MISTRAL_API_KEY="$SIRIUS_MISTRAL_API_KEY" sirius-moderation`


### Test endpoints
`curl 'http://0.0.0.0:8000/score' -X POST -H 'Content-Type: application/json' -d '{"text": "patisserie ou cuisine"}'`

`curl 'http://0.0.0.0:8000/expose' -X POST -H 'Content-Type: application/json' -d '{"text": "Il faut se lever tôt le matin et tenir toute la journée mais ça vaut le coup! Surtout si tu es en fauteuil roulant"}'`


### Stop and remove image
`docker stop moderation && docker rm moderation`


## 3. Deploy on OVHcloud
[TODO]