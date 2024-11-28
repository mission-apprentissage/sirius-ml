# SIRIUS-CORRECTION

## 0. Add environment variable
The application depends on this secret environment variables:
- $SIRIUS_MISTRAL_API_KEY

## 1. Test application

### Install the requirements

```
$ cd correction && python3 -m venv .venv && source .venv/bin/activate
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
# Get correction
$ curl 'http://127.0.0.1:8000/correct' -X POST -H 'Content-Type: application/json' -d '{"text": "cuisinner"}'
```

## 2. Create image
### Build image
```
cd correction && docker buildx build --platform linux/amd64 -t sirius-correction .
```
### Run image
```
docker run --rm -it --user=42420:42420 -p 8000:8000 --name correction -e SIRIUS_MISTRAL_API_KEY="$SIRIUS_MISTRAL_API_KEY" sirius-correction
```
### Test docker endpoints
```
# Get correction
$ curl 'http://0.0.0.0:8000/correct' -X POST -H 'Content-Type: application/json' -d '{"text": "cuisinner"}'
```

### Stop and remove image
```
$ docker stop correction 
$ docker rmi sirius-correction
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
$ docker tag sirius-correction registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-correction
$ docker push registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-correction
```

### Deploy
```
# Run API app
$ ovhai app run --name sirius-correction --cpu 1 --default-http-port 8000 --unsecure-http -e SIRIUS_MISTRAL_API_KEY="$SIRIUS_MISTRAL_API_KEY" registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-correction

# Stop app
$ ovhai app stop <ovh-id>

# Delete app
$ ovhai app delete <ovh-id>

# Check log
$ ovhai app logs <ovh-id>
```

### Test OVH endpoint
```
# Get correction
$ curl 'https://<ovh-id>.app.gra.ai.cloud.ovh.net/correct' -X POST -H 'Content-Type: application/json' -d '{"text": "cuisinner"}'
{"texte":"cuisinner","correction":"cuisinier","justification":"Le mot correct est 'cuisinier', qui désigne une personne qui cuisine."}
```