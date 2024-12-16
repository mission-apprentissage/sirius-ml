# SIRIUS-EXPOSITION

## 0. Add environment variable
The application depends on this secret environment variables:
- $SIRIUS_MISTRAL_API_KEY

## 1. Test application

### Install the requirements

```
$ cd exposition && python3 -m venv .venv && source .venv/bin/activate
$ pip install -r requirements.txt
```

### Start the application
```
# Start server
$ fastapi dev api.py

# Kill all server (if blocked)
$ sudo lsof -t -i tcp:8000 | xargs kill -9
```

### Test local endpoints
```
# Get exposition
$ curl 'http://127.0.0.1:8000/correct' -X POST -H 'Content-Type: application/json' -d '{"text": "cuisinner"}'
```

## 2. Create image
### Build image
```
cd exposition && docker buildx build --platform linux/amd64 -t sirius-exposition .
```
### Run image
```
docker run --rm -it --user=42420:42420 -p 8000:8000 --name exposition -e SIRIUS_MISTRAL_API_KEY="$SIRIUS_MISTRAL_API_KEY" sirius-exposition
```
### Test docker endpoints
```
# Get exposition
$ curl 'http://0.0.0.0:8000/expose' -X POST -H 'Content-Type: application/json' -d '{"text": "cuisinner"}'

# Exposition
$ curl 'http://0.0.0.0:8000/expose' -X POST -H 'Content-Type: application/json' -d '{"text": "Il faut se lever tôt le matin et tenir toute la journée mais ça vaut le coup! Surtout si tu es en fauteuil roulant"}'
```

### Stop and remove image
```
$ docker stop exposition
$ docker rmi sirius-exposition
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
$ docker tag sirius-exposition registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-exposition
$ docker push registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-exposition
```

### Deploy
```
# Run API app
$ ovhai app run --name sirius-exposition --cpu 1 --default-http-port 8000 --unsecure-http -e SIRIUS_MISTRAL_API_KEY="$SIRIUS_MISTRAL_API_KEY" registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-exposition

# Stop app
$ ovhai app stop <ovh-id>

# Delete app
$ ovhai app delete <ovh-id>

# Check log
$ ovhai app logs <ovh-id>
```

### Test OVH endpoint
```
# Get exposition
$ curl 'https://<ovh-id>.app.gra.ai.cloud.ovh.net/expose' -X POST -H 'Content-Type: application/json' -d '{"text": "cuisinner"}'
{"texte":"cuisinner","correction":"cuisiner","justification":"Correction de la faute d'orthographe."}
```