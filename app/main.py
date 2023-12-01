from contextlib import asynccontextmanager

import pymongo
import uvicorn
from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.requests import Request
from fastapi.responses import Response

from app import tasks_router

task_collection = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global task_collection
    client = MongoClient('mongodb://127.0.0.1:27017/usage?retryWrites=true&w=majority')
    db = client['tasks']
    task_collection = db['task']
    task_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(tasks_router.router)


@app.middleware("http")
async def errors_handling(request: Request, call_next):
    """
    middleware to handle exceptions
    """
    try:
        return await call_next(request)
    except Exception as exc:
        return Response(status_code=500, content={'reason': str(exc)})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5050, reload=True)
