from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    mongodb_url = 'mongodb://127.0.0.1:27017/usage?retryWrites=true&w=majority'
    mongo_database_name = 'tasks'
    mongo_collection_name = 'task'


@lru_cache()
def get_settings():
    return Settings()
