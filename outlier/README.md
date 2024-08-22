# SIRIUS-OUTLIER

## 1. Test application

### Install the requirements

`cd outlier && python3 -m venv .venv && source .venv/bin/activate`

`pip install -r requirements.txt`

### Start the application
`fastapi dev app/api.py`

### Debug
Kill all server
`sudo lsof -t -i tcp:8000 | xargs kill -9`

### Test endpoints

#### Scoring
`curl http://127.0.0.1:8000/score -X POST -H "Content-Type: multipart/form-data" -F "file=@./outlier/dataset/sample.csv"`

#### Detection
`curl 'http://127.0.0.1:8000/detect' -X POST -H 'Content-Type: application/json' -d '{"scores":[-9.890680333249605,-8.81517297694887,-10.817086031345966,-9.134718245421285,-9.136104401859312,-10.10892008829345,-9.246591666943132], "percent": 1}'`

## 2. Create image

### Build image
`docker buildx build -t sirius-outlier .`

### Run image
`docker run -p 8000:8000 --name outlier sirius-outlier`


### Test endpoints
`curl http://0.0.0.0:8000/score -X POST -H "Content-Type: multipart/form-data" -F "file=@./dataset/campagne.csv" -F "id=test"`

`curl 'http://0.0.0.0:8000/detect' -X POST -H 'Content-Type: application/json' -d '{"scores":[-9.890680333249605,-8.81517297694887,-10.817086031345966,-9.134718245421285,-9.136104401859312,-10.10892008829345,-9.246591666943132], "percent": 1}'`


### Stop and remove image
`docker stop outlier && docker rm outlier`


## 3. Deploy on OVHcloud
[TODO]