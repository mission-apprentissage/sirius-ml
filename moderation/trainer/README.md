# SIRIUS-MODERATION

## 0. Add environment variable
The application depends on this secret environment variables:
- $SIRIUS_AI_USER
- $SIRIUS_AI_PWD
- $SIRIUS_AI_TOKEN
- $SIRIUS_DB_API
- $SIRIUS_HF_TOKEN
- $SIRIUS_MISTRAL_API_KEY

## 1. Test application

### Install the requirements
```
$ python3 -m venv .venv && source .venv/bin/activate
$ pip install -r requirements.txt
```

### Start the application
```
# Start app
$ python trainer.py
```

## 2. Create image

### Build image
```
docker buildx build --platform linux/amd64 -t sirius-trainer .
```
### Run image
```
docker run --rm -it --user=42420:42420 --name trainer -e SIRIUS_DB_API="$SIRIUS_DB_API" -e SIRIUS_HF_TOKEN="$SIRIUS_HF_TOKEN" -e SIRIUS_MISTRAL_API_KEY="$SIRIUS_MISTRAL_API_KEY" -e table="verbatims" -e repo="apprentissage-sirius/verbatims" sirius-trainer
```

### Stop and remove image
```
$ docker stop trainer 
$ docker rmi sirius-trainer
```

## 3. Deploy on [OVHcloud](https://help.ovhcloud.com/csm/en-public-cloud-ai-deploy-build-use-custom-image?id=kb_article_view&sysparm_article=KB0057405)

### Install [ovhai client](https://help.ovhcloud.com/csm/en-gb-public-cloud-ai-cli-install-client?id=kb_article_view&sysparm_article=KB0047844)
```
# Install client
$ curl https://cli.gra.ai.cloud.ovh.net/install.sh | bash && source $HOME/.bashrc

# Login client
$ ovhai login -u $SIRIUS_AI_USER -p $SIRIUS_AI_PWD
```

### Push docker image to OVHcloud
```
# Add a new registry into OVHcloud AI Tools (if not exist)
$ ovhai registry add registry.gra.ai.cloud.ovh.net

# Push your image
$ docker login -u $SIRIUS_AI_USER -p $SIRIUS_AI_PWD registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59
$ docker tag sirius-trainer registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-trainer
$ docker push registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-trainer
```

### Deploy
```
# Run trainer job
$ ovhai job run --name sirius-trainer --flavor l4-1-gpu --gpu 1 --default-http-port 8000 --unsecure-http -e SIRIUS_DB_API="$SIRIUS_DB_API" -e SIRIUS_HF_TOKEN="$SIRIUS_HF_TOKEN" -e SIRIUS_MISTRAL_API_KEY="$SIRIUS_MISTRAL_API_KEY" -e table="verbatims" -e repo="apprentissage-sirius/verbatims" registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-trainer


# Rerun trainer job
$ ovhai job rerun <ovh-id>

# Check log
$ ovhai job logs <ovh-id>
```

### Run job endpoint
see API doc: https://gra.training.ai.cloud.ovh.net/

```
$ curl --request PUT --url https://gra.training.ai.cloud.ovh.net/v1/job/<ovh-id>/start -H 'Accept: application/json' -H 'Authorization: Bearer '$SIRIUS_AI_TOKEN -H 'Content-Type: application/json'
```