from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from pymongo.errors import DuplicateKeyError
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from app.models import TaskModel

router = APIRouter()


@router.get("/", description="Returns all tasks")
async def find_all_tasks():
    from main import task_collection
    # noinspection PyGlobalUndefined
    global task_collection
    pipeline = [
        {"$addFields": {"id": {"$toString": "$_id"}}},
        {'$unset': ['_id']},
    ]
    return list(task_collection.aggregate(pipeline))


@router.get("/tasks", description="Search tasks with field considered as string")
def find_tasks_get(request: Request):
    """
    In order to search the items regarding the data types as string you should use this endpoint
    :param request: Search criteria (they are all considered as string) are sent in query params
    :return: Result
    """
    params = jsonable_encoder(request.query_params)
    from main import task_collection
    # noinspection PyGlobalUndefined
    global task_collection
    pipeline = [
        {"$addFields": {"id": {"$toString": "$_id"}}},
        {'$unset': ['_id']},
        {'$match': params}
    ]
    return list(task_collection.aggregate(pipeline))


@router.post("/tasks/", description="Search tasks with field types considered")
def find_tasks_post(request: Request, search_criteria=Body(...), ):
    """
    In order to search the items regarding the data types (type safe) you should use this endpoint
    :param request:
    :param search_criteria: Search Criteria (all user types are considered as entered)
    :return: Result
    """
    from main import task_collection
    # noinspection PyGlobalUndefined
    global task_collection

    pipeline = [
        {"$addFields": {"id": {"$toString": "$_id"}}},
        {'$unset': ['_id']},
        {'$match': search_criteria}
    ]
    return list(task_collection.aggregate(pipeline))


@router.post("/", status_code=status.HTTP_201_CREATED, description="Adds a task to database")
async def add_task_data(
        request: Request,
        task=Body(...),
):
    try:
        TaskModel.model_validate(task)
    except ValidationError as exc:
        raise HTTPException(detail='validation error', status_code=status.HTTP_400_BAD_REQUEST)

    from main import task_collection
    # noinspection PyGlobalUndefined
    global task_collection

    try:
        t = task_collection.insert_one(task)
        # new_task = task_collection.find_one({"_id": t.inserted_id}, {'_id': False})
        return str(t.inserted_id)
    except DuplicateKeyError as dke:
        raise HTTPException(detail=dke.details.get("errmsg", "duplicate id"), status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return HTTPException(detail=ex.message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/{id}", description="Updates a task")
async def update_task_data(id: str, req=Body(...)):
    from main import task_collection
    # noinspection PyGlobalUndefined
    global task_collection

    data = {k: v for k, v in req.items() if v is not None}
    task = task_collection.find_one({"_id": ObjectId(id)})
    if task:
        updated_task = task_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_task:
            return Response(content=f"Task with ID: {id} update is successful")
        else:
            raise HTTPException(detail=f"Task with ID: {id} update is unsuccessful",
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    raise HTTPException(detail="task not found", status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{id}")
async def delete_task_data(id: str):
    from main import task_collection
    # noinspection PyGlobalUndefined
    global task_collection

    task_to_delete = task_collection.find_one({"_id": ObjectId(id)})
    if task_to_delete:
        task_collection.delete_one({"_id": ObjectId(id)})
        return Response(f"Task with ID: {id} removed")
    else:
        raise HTTPException(detail="task not found", status_code=status.HTTP_404_NOT_FOUND)
