from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_url: str = 'mongodb://127.0.0.1:27017/usage?retryWrites=true&w=majority'
    mongo_database_name: str = 'tasks'
    mongo_collection_name: str = 'task'


@lru_cache()
def get_settings():
    return Settings()
