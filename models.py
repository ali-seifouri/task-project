from pydantic import BaseModel, Field


class TaskModel(BaseModel):
    # id: int = Field(unique=True)
    name: str
    description: str
    status: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        extra = 'allow'

