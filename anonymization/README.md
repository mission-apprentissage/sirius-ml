# SIRIUS-ANONYMIZATION

## 0. Add environment variable
The application depends on this secret environment variables:
- $SIRIUS_MISTRAL_API_KEY

## 1. Test application

### Install the requirements

```
$ cd anonymization && python3 -m venv .venv && source .venv/bin/activate
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
# Get anonymization
$ curl 'http://127.0.0.1:8000/anonymize' -X POST -H 'Content-Type: application/json' -d '{"text": "Jean Dupont et Marie Durand ont assisté à la réunion."}'
```

## 2. Create image
### Build image
```
cd anonymization && docker buildx build --platform linux/amd64 -t sirius-anonymization .
```
### Run image
```
docker run --rm -it --user=42420:42420 -p 8000:8000 --name anonymization -e SIRIUS_MISTRAL_API_KEY="$SIRIUS_MISTRAL_API_KEY" sirius-anonymization
```
### Test docker endpoints
```
# Get anonymization
$ curl 'http://0.0.0.0:8000/anonymize' -X POST -H 'Content-Type: application/json' -d '{"text": "Jean Dupont et Marie Durand ont assisté à la réunion."}'
```

### Stop and remove image
```
$ docker stop anonymization 
$ docker rmi sirius-anonymization
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
$ docker tag sirius-anonymization registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-anonymization
$ docker push registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-anonymization
```

### Deploy
```
# Run API app
$ ovhai app run --name sirius-anonymization --cpu 1 --default-http-port 8000 --unsecure-http -e SIRIUS_MISTRAL_API_KEY="$SIRIUS_MISTRAL_API_KEY" registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-anonymization

# Stop app
$ ovhai app stop <ovh-id>

# Delete app
$ ovhai app delete <ovh-id>

# Check log
$ ovhai app logs <ovh-id>
```

### Test OVH endpoint
```
# Get anonymization
$ curl 'https://<ovh-id>.app.gra.ai.cloud.ovh.net/anonymize' -X POST -H 'Content-Type: application/json' -d '{"text": "Jean Dupont et Marie Durand ont assisté à la réunion."}'

{"texte":"Jean Dupont et Marie Durand ont assisté à la réunion.","anonymisation":"Ils ont assisté à la réunion.","justification":"Les noms propres 'Jean Dupont' et 'Marie Durand' ont été remplacés par le pronom 'Ils' pour anonymiser le texte."}
```