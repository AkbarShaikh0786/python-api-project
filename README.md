# Python API Project

A small [FastAPI](https://fastapi.tiangolo.com/) service that exposes system
metrics, log analysis, and AWS (S3) info over HTTP. Containerized with
Docker for easy local run or deployment.

## Project structure

```
python-api-project/
├── Dockerfile
├── main.py                    # Entry point — runs the app with uvicorn
├── requirements.txt           # Python dependencies
├── app.log                    # Sample log file (used by the /logs endpoint by default)
├── app/
│   └── api.py                 # FastAPI app instance, root routes, router registration
├── routers/
│   ├── metrics.py             # /metrics endpoint
│   ├── logs.py                # /logs endpoint
│   └── aws.py                 # /aws/s3, /aws/ec2 endpoints
└── services/
    ├── metrics_service.py     # CPU / memory / disk usage logic
    ├── logs_service.py        # Log file parsing logic
    └── aws_service.py         # S3 bucket lookup logic (via boto3)
```

## Requirements

- Docker installed and running
- If running the AWS endpoints (`/aws/s3`, `/aws/ec2`) against real AWS
  resources, valid AWS credentials available to the container (see
  [AWS credentials](#aws-credentials) below)

## Build the image

```bash
docker build -t python-app:latest .
```

This installs dependencies from `requirements.txt` into a
`python:3.13-slim` base image and copies in the application code.

## Run the container

```bash
docker run -d -p 8000:8000 python-app:latest
```

- `-d` runs it in the background
- `-p 8000:8000` maps container port `8000` (where uvicorn listens) to the
  same port on your host

Check it's running:

```bash
docker ps
```

## API endpoints

Once running, interactive docs are available at:

```
http://localhost:8000/docs
```

(or `http://<server-ip>:8000/docs` on a remote host — make sure port 8000
is open in your firewall/security group)

| Method | Path         | Description                                              |
|--------|--------------|-----------------------------------------------------------|
| GET    | `/`          | Basic hello-world health check                             |
| GET    | `/health`    | Returns `{"status": "ok"}`                                 |
| GET    | `/metrics`   | Current CPU, memory, and disk usage of the container       |
| GET    | `/logs`      | Counts of INFO/WARNING/ERROR lines in a log file. Optional `?file=` query param; defaults to the bundled `app.log` |
| GET    | `/aws/s3`    | Lists S3 buckets, split into new (<90 days old) and old     |
| GET    | `/aws/ec2`   | Placeholder — not yet implemented                          |

### Examples

```bash
curl http://localhost:8000/metrics
curl http://localhost:8000/logs
curl "http://localhost:8000/logs?file=/app/app.log"
curl http://localhost:8000/aws/s3
```

## AWS credentials

The `/aws/s3` endpoint uses `boto3`, which looks for AWS credentials in the
standard locations (environment variables, `~/.aws/credentials`, or an
attached IAM role if running on EC2). To pass credentials into the
container explicitly:

```bash
docker run -d -p 8000:8000 \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  -e AWS_DEFAULT_REGION=your_region \
  python-app:latest
```

If running on an EC2 instance with an attached IAM role that has S3
permissions, no explicit credentials are needed — boto3 picks up the role
automatically.

## Stopping / rebuilding

```bash
docker ps                # find the container ID
docker stop <container>
docker rm <container>

# after making code changes:
docker build -t python-app:latest .
docker run -d -p 8000:8000 python-app:latest
```

## Running locally without Docker (optional)

```bash
pip install -r requirements.txt
python main.py
```

Note: `main.py` runs uvicorn with `reload=True`, which is intended for
local development, not production use inside the container.
