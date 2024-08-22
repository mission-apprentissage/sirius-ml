# SIRIUS-OUTLIER

## 1. Test application

### Install the requirements
```
$ cd moderation && python3 -m venv .venv && source .venv/bin/activate`
$ pip install -r requirements.txt
```

### Start the application
```
# Start server
$ fastapi dev app/api.py

# Kill all server
$ sudo lsof -t -i tcp:8000 | xargs kill -9
```

### Test endpoints
```
# Scoring
curl http://127.0.0.1:8000/score -X POST -H "Content-Type: multipart/form-data" -F "file=@./outlier/dataset/sample.csv"

# Detection
curl 'http://127.0.0.1:8000/detect' -X POST -H 'Content-Type: application/json' -d '{"scores":[-9.890680333249605,-8.81517297694887,-10.817086031345966,-9.134718245421285,-9.136104401859312,-10.10892008829345,-9.246591666943132], "percent": 1}'
```

## 2. Create image

### Build image
```
docker buildx build --platform linux/amd64 -t sirius-outlier .
```
### Run image
```
docker run --rm -it --user=42420:42420 -p 8000:8000 --name outlier sirius-outlier
```

### Test endpoints
```
# Score
curl http://0.0.0.0:8000/score -X POST -H "Content-Type: multipart/form-data" -F "file=@./dataset/sample.csv"

# Detection
curl 'http://0.0.0.0:8000/detect' -X POST -H 'Content-Type: application/json' -d '{"scores":[-9.890680333249605,-8.81517297694887,-10.817086031345966,-9.134718245421285,-9.136104401859312,-10.10892008829345,-9.246591666943132], "percent": 1}'
```

### Stop and remove image
```
$ docker stop outlier && docker rm outlier
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
# Add a new registry into OVHcloud AI Tools
$ ovhai registry add registry.gra.ai.cloud.ovh.net

# Push your image
$ docker login registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59
$ docker tag sirius-outlier registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-outlier
$ docker push registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-outlier
```

### Deploy
```
# Run app
$ ovhai app run --name sirius-outlier --flavor l4-1-gpu --gpu 1 --replicas 1 --default-http-port 8000 --unsecure-http registry.gra.ai.cloud.ovh.net/deae30132f2745cda273f1ebce462f59/sirius-outlier

# Stop app
$ ovhai app stop <ovh-id>

# Delete app
$ ovhai app delete <ovh-id>
```

### Test endpoint
```
# Score
curl https://<ovh-id>.app.gra.ai.cloud.ovh.net/score -X POST -H "Content-Type: multipart/form-data" -F "file=@./dataset/sample.csv"

# Detect
curl https://<ovh-id>.app.gra.ai.cloud.ovh.net/detect -X POST -H 'Content-Type: application/json' -d '{"scores":[-9.890680333249605,-8.81517297694887,-10.817086031345966,-9.134718245421285,-9.136104401859312,-10.10892008829345,-9.246591666943132], "percent": 1}'`
```