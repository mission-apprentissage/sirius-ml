# SIRIUS-DATABASE

## 0. Add environment variable
The application depends on this secret environment variables:
- $SIRIUS_DB_URL

## 1. Test application

### Install the requirements

```
$ cd database && python3 -m venv .venv && source .venv/bin/activate
$ pip install -r requirements.txt
```

### Start the application
```
# Start server
$ fastapi dev api.py

# Kill all server (if blocked)
$ sudo lsof -t -i tcp:8000 | xargs kill -9
```


### Authorize ip adress (database provider in dev mode)
Check fastapi ip adress after running

### Test local endpoints
```
# Load database
$ curl 'http://127.0.0.1:8000/load' -X POST -H 'Content-Type: application/json' -d '{"table": "verbatims"}'
```

## 2. Create image
### Build image
```
cd database && docker buildx build --platform linux/amd64 -t sirius-database .
```
### Run image
```
docker run --rm -it --user=42420:42420 -p 8000:8000 --name database -e SIRIUS_DB_URL="$SIRIUS_DB_URL" sirius-database
```
### Test docker endpoints
```
# Load database
$ curl 'http://0.0.0.0:8000/load' -X POST -H 'Content-Type: application/json' -d '{"table": "verbatims"}'
```

### Stop and remove image
```
$ docker stop moderation 
$ docker rmi sirius-database
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
$ docker tag sirius-database registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-database
$ docker push registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-database
```

### Deploy
```
# Run API app
$ ovhai app run --name sirius-database --cpu 1 --default-http-port 8000 --unsecure-http -e SIRIUS_DB_URL="$SIRIUS_DB_URL" registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-database

# Stop app
$ ovhai app stop <ovh-id>

# Delete app
$ ovhai app delete <ovh-id>

# Check log
$ ovhai app logs 04609d3d-99fb-4017-b20c-51331b494cfe
```

### Test OVH endpoint
```
# Load database
$ curl 'https://04609d3d-99fb-4017-b20c-51331b494cfe.app.gra.ai.cloud.ovh.net/load' -X POST -H 'Content-Type: application/json' -d '{"table": "verbatims"}'
```