from fastapi import FastAPI
import logging

app = FastAPI()
logger = logging.getLogger("uvicorn")


@app.get("/")
async def read_root():
	logger.info("Root endpoint hit")
	return {"message": "Hello, DevOps!"}


@app.get("/health")
async def health():
	return {"status": "ok"}
