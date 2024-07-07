import redis


class Database(object):
    def __init__(self, config=None) -> None:
        self._config = config
        self._db = redis.Redis(host="localhost", port=6379, decode_responses=True)

    def cache_val(self, key, val):
        return self._db.set(key, val)

    def retrieve_val(self, key):
        return self._db.get(key)

    # def cache_mapping(self, mapping):
