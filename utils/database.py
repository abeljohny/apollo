import time
import uuid
from datetime import datetime

import redis

from constants import Defaults, Formatting
from utils.prompt import Prompt


class Database(object):
    """Manages Database read-writes"""

    def __init__(self):
        self._redis = redis.Redis(
            host=Defaults.DATABASE_HOST.value,
            port=Defaults.DATABASE_PORT.value,
            decode_responses=True,
        )

    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())

    @property
    def instance(self):
        return self._redis

    @staticmethod
    def format_timestamp(timestamp):
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    def write_conversation_to_db(self, prompt: str, conversation: str):
        key = Database.generate_uuid()
        return self._redis.hset(
            key,
            mapping={
                "key": key,
                "prompt": prompt,
                "truncated_prompt": Prompt.truncate_prompt(prompt),
                "conversation": Formatting.CONVERSATION.value.format(
                    prompt=prompt, conversation=conversation
                ),
                "timestamp": Database.format_timestamp(time.time()),
            },
        )
