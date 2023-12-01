from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request

from pymongo import MongoClient
from starlette.responses import JSONResponse

from tasks_router import router as task_router1
from config import get_settings

task_collection = None

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global task_collection
    client = MongoClient(settings.mongodb_url)
    db = client[settings.mongo_database_name]
    task_collection = db[settings.mongo_collection_name]
    # if we want to add a custom id column with unique index we should add the line below (if we dont want to use the
    # ObjectID as the main id in business)
    # task_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(task_router1)


@app.middleware("http")
async def errors_handling(request: Request, call_next):
    """
    middleware to handle exceptions
    """
    try:
        return await call_next(request)
    except Exception as exc:
        return JSONResponse(status_code=500, content={'reason': str(exc)})


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
