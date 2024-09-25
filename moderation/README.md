# SIRIUS-MODERATION

## 0. Add environment variable
The application depends on this secret environment variables:
- $SIRIUS_DB_URL
- $SIRIUS_HF_TOKEN
- $SIRIUS_MISTRAL_API_KEY

## 1. Test application

### Install the requirements

```
$ cd moderation && python3 -m venv .venv && source .venv/bin/activate
$ pip install -r requirements.txt
```

### Start the application
```
# Start server
$ fastapi dev app/api.py

# Kill all server (if blocked)
$ sudo lsof -t -i tcp:8000 | xargs kill -9
```


### Authorize ip adress (database provider in dev mode)
Check fastapi ip adress after running

### Test local endpoints
```
# Load dataset
$ curl 'http://127.0.0.1:8000/load' -X POST -H 'Content-Type: application/json' -d '{"table": "verbatims", "repo":"apprentissage-sirius/verbatims"}'

# Update dataset
$ curl 'http://127.0.0.1:8000/update' -X POST -H 'Content-Type: application/json' -d '{"table": "verbatims", "repo": "apprentissage-sirius/verbatims"}'

# Moderate short text
$ curl 'http://127.0.0.1:8000/score' -X POST -H 'Content-Type: application/json' -d '{"text": "patisserie ou cuisine"}'

# Moderate text with rules
$ curl 'http://127.0.0.1:8000/score' -X POST -H 'Content-Type: application/json' -d '{"text": "tkt, ça va le faire si tu supportes l’OM !", "rules": "\n- Il suffit de supporter l’OM\n"}'

# Check text exposition
$ curl 'http://127.0.0.1:8000/expose' -X POST -H 'Content-Type: application/json' -d '{"text": "Il faut se lever tôt le matin et tenir toute la journée mais ça vaut le coup! Surtout si tu es en fauteuil roulant"}'
```

## 2. Create image

### Build image
```
docker buildx build --platform linux/amd64 -t sirius-moderation .
```
### Run image
```
docker run --rm -it --user=42420:42420 -p 8000:8000 --name moderation -e SIRIUS_DB_URL="$SIRIUS_DB_URL" -e SIRIUS_HF_TOKEN="$SIRIUS_HF_TOKEN" -e SIRIUS_MISTRAL_API_KEY="$SIRIUS_MISTRAL_API_KEY" sirius-moderation
```
### Test docker endpoints
```
# Load dataset
$ curl 'http://0.0.0.0:8000/load' -X POST -H 'Content-Type: application/json' -d '{"table": "verbatims", "repo":"apprentissage-sirius/verbatims"}'

# Update dataset
$ curl 'http://0.0.0.0:8000/update' -X POST -H 'Content-Type: application/json' -d '{"table": "verbatims", "repo": "apprentissage-sirius/verbatims"}'

# Score
$ curl 'http://0.0.0.0:8000/score' -X POST -H 'Content-Type: application/json' -d '{"text": "patisserie ou cuisine"}'

# Exposition
$ curl 'http://0.0.0.0:8000/expose' -X POST -H 'Content-Type: application/json' -d '{"text": "Il faut se lever tôt le matin et tenir toute la journée mais ça vaut le coup! Surtout si tu es en fauteuil roulant"}'
```

### Stop and remove image
```
$ docker stop moderation && docker rm moderation
```

## 3. Deploy on [OVHcloud](https://help.ovhcloud.com/csm/en-public-cloud-ai-deploy-build-use-custom-image?id=kb_article_view&sysparm_article=KB0057405)

### Install [ovhai client](https://help.ovhcloud.com/csm/en-gb-public-cloud-ai-cli-install-client?id=kb_article_view&sysparm_article=KB0047844)
```
# Install client
$ curl https://cli.gra.ai.cloud.ovh.net/install.sh | bash && source $HOME/.bashrc

# Login client
$ ovhai login
```

### Push docker image to OVHcloud
```
# Add a new registry into OVHcloud AI Tools (if not exist)
$ ovhai registry add registry.gra.ai.cloud.ovh.net

# Push your image
$ docker login registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59
$ docker tag sirius-moderation registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-moderation
$ docker push registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-moderation
```

### Deploy
```
# Run app
$ ovhai app run --name sirius-moderation --flavor ai1-1-cpu --cpu 8 --replicas 1 --default-http-port 8000 --unsecure-http -e SIRIUS_DB_URL="$SIRIUS_DB_URL" -e SIRIUS_HF_TOKEN="$SIRIUS_HF_TOKEN" -e SIRIUS_MISTRAL_API_KEY="$SIRIUS_MISTRAL_API_KEY" registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-moderation

# Stop app
$ ovhai app stop <ovh-id>

# Delete app
$ ovhai app delete <ovh-id>

# Chek log
$ ovhai app logs <ovh-id>
```

### Test OVH endpoint
```
# Load dataset
$ curl 'https://b22b3d95-f4d8-48a5-974d-4b0ead6a1bcd.app.gra.ai.cloud.ovh.net/load' -X POST -H 'Content-Type: application/json' -d '{"table": "verbatims", "repo":"apprentissage-sirius/verbatims"}'

# Update dataset
$ curl 'https://b22b3d95-f4d8-48a5-974d-4b0ead6a1bcd.app.gra.ai.cloud.ovh.net/update' -X POST -H 'Content-Type: application/json' -d '{"table": "verbatims", "repo": "apprentissage-sirius/verbatims"}'

# Score
$ curl 'https://b22b3d95-f4d8-48a5-974d-4b0ead6a1bcd.app.gra.ai.cloud.ovh.net/score' -X POST -H 'Content-Type: application/json' -d '{"text": "patisserie ou cuisine"}'

# Exposition
$ curl 'https://b22b3d95-f4d8-48a5-974d-4b0ead6a1bcd.app.gra.ai.cloud.ovh.net/expose' -X POST -H 'Content-Type: application/json' -d '{"text": "Il faut se lever tôt le matin et tenir toute la journée mais ça vaut le coup! Surtout si tu es en fauteuil roulant"}'
```