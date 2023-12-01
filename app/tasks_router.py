from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from pymongo.errors import DuplicateKeyError
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from app.models import TaskModel

router = APIRouter()


@router.get("/")
async def read_root():
    from main import task_collection
    # noinspection PyGlobalUndefined
    global task_collection
    tasks = [t for t in task_collection.find({}, {'_id': False})]
    return tasks


@router.get("/tasks/")
def read_item(request: Request):
    params = jsonable_encoder(request.query_params)
    from main import task_collection
    # noinspection PyGlobalUndefined
    global task_collection
    tasks = [t for t in task_collection.find(params, {'_id': False})]
    return tasks


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_task_data(
        request: Request,
        task=Body(...),
):
        try:
            TaskModel.model_validate(task)
        except ValidationError as exc:
            return Response(content='validation error', status_code=status.HTTP_400_BAD_REQUEST)

        from main import task_collection
        # noinspection PyGlobalUndefined
        global task_collection

        try:
            t = task_collection.insert_one(task)
            new_task = task_collection.find_one({"_id": t.inserted_id}, {'_id': False})
            return new_task
        except DuplicateKeyError as dke:
            return dke.details.get("errmsg", "duplicate id")
        except Exception as ex:
            return ex.message

