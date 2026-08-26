from fastapi import FastAPI
from routers import metrics, aws, logs

app = FastAPI(
    title="Python API",
    description="Python API for system metrics, AWS usage, and log analysis.",
    version="1.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/")
def hello():
    return {"message": "Hello Dosto, this is the page for python API's"}


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(metrics.router)
app.include_router(logs.router)
app.include_router(aws.router, prefix="/aws")
