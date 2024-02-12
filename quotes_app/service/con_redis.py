import os
import pickle

import redis
from dotenv import load_dotenv

load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_USER = os.getenv("REDIS_USER")
REDIS_PW = os.getenv("REDIS_PW")
REDIS_DB = os.getenv("REDIS_DB")

redis_connector = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    username=REDIS_USER,
    password=REDIS_PW,
    db=REDIS_DB,
)


def redis_set(key: str, val, connection=redis_connector) -> None:
    connection.set(key, pickle.dumps(val), ex=900)
    # print(f"wrote to db {key=}, {val=}")


def redis_get(key: str, connection=redis_connector):
    val = connection.get(key)
    if val:
        return pickle.loads(val)
    else:
        return


if __name__ == "__main__":
    print(REDIS_PORT, REDIS_USER, REDIS_DB, REDIS_HOST, REDIS_PW)
