from fastapi import FastAPI

app = FastAPI(
    title="Bill Extraction API",
    description="Bajaj Health Datathon",
    version="1.0.0"
)

__all__ = ['app']

