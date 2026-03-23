"""Sample FastAPI application for ADHD pipeline demo."""
from fastapi import FastAPI

app = FastAPI(title="Sample Monorepo API")


@app.get("/health")
def health():
    return {"status": "ok"}
