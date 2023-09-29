# CONTRIBUTING

## How to buils a Dockerfile locally 

docker build -t IMAGE_NAME:VERSION .

## How to run Dockerfile locally

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run --host 0.0.0.0"
```

## How to run rq-worker 

```
docker run -w /app rest-api-recording-email sh -c "rq worker -u REDIS_URL QUEUE_NAME"
```
