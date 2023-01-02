from ast import literal_eval
from asyncio import Lock

from aioredis import Redis

from .logger import LOGS


class DataBase(Redis):
    def __init__(self):
        self.lock = Lock()

    def finish_setup(self, host, password, **kwargs):
        if ":" in host:
            data = host.split(":")
            host = data[0]
            port = int(data[1])
        if host.startswith("http"):
            LOGS.error("Your REDIS_URI should not start with http..")
            quit()
        elif not (host and port):
            LOGS.error("Port Number not found, Correct your REDIS_URI Variable.")
            quit()
        try:
            LOGS.info("Trying to Connect With Redis")
            super().__init__(
                host=host,
                port=port,
                password=password,
                encoding="utf-8",
                decode_responses=True,
                **kwargs,
            )
            if not self.ping():
                raise Exception("Error while Pinging the Redis DB")
            else:
                LOGS.info("Successfully Connected to Redis")
        except Exception as e:
            LOGS.exception(e)
            LOGS.ctitical(f"Error while Connecting to Redis: {e}")
            quit()

    @staticmethod
    def load(data):
        if not data:
            return data
        try:
            return literal_eval(data)
        except Exception:
            return data

    async def get_key(self, key):
        async with self.lock:
            data = await self.get(key)
            return self.load(data)

    async def del_key(self, key):
        async with self.lock:
            return await self.delete(key)

    async def set_key(self, key, value):
        async with self.lock:
            return await self.set(key, str(value))
