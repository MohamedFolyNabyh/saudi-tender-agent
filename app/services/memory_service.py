# # 

# import json
# import logging
# from typing import List,Dict
# import redis 
# from app.config.settings import settings


# logger=logging.getLogger(__name__)

# class MemoryService:
#     def __init__(self):
#         self.client=redis.Redis(
#             host=settings.REDIS_HOST,
#             port=settings.REDIS_PORT,
#             username="default",
#             password=settings.REDIS_PASSWORD,
#             db=0,
#             decode_responses=True
#         )

#         logger.info("Redis connect successfully")
#         def _get_key(self, session_id:str) ->str:

#             """
#             generate Redis key
#             """
#             return f"chat {session_id}"
#         def save_message(self,session_id:str,role:str,content:str) ->None:
#             key=self._get_key(session_id)
#             message={
#                 "role":role,
#                 "content":content
#             }
#             self.client.rpush(key,json.dumps(message))

#             self.client.expire(key,settings.REDIS_TTL)

#         def save_conversation(self,session_id:str,messages:List[Dict]) ->None:
#             key=self._get_key(session_id)
#             if not messages:
#                 return
#             values=[json.dumps(message) for message in messages]

#             self.client.rpush(key,
#             *values)
#             self.client.expire(key,
#             settings.REDIS_TTL
#             )
#         def load_history(self,session_id:str) ->List[Dict]:
#             key=self._get_key(session_id)
#             history=self.client.lrange(
#                 key,
#                 0,
#                 -1
#             )
#             return [
#                 json.loads(item) for item in history
#             ]
#         def get_last_messages(self,session_id:str,limit:int=10) ->List[Dict]:
#             key=self._get_key(session_id)

#             history=self.client.lrange(
#                 key,
#                 -limit,
#                 -1
#             )
#             return [
#                 json.loads(item) for item in history
#             ]
        
#     def clear_history(
#         self,
#         session_id: str
#     ) -> None:
#         """
#         Delete conversation.
#         """

#         key = self._get_key(session_id)

#         self.client.delete(key)

#         logger.info(
#             "Conversation deleted: %s",
#             session_id
#         )

#     def session_exists(self,session_id: str) -> bool:
#         """
#         Check if session exists.
#         """

#         return bool(
#             self.client.exists(
#                 self._get_key(session_id)
#             )
#         )

#     def ping(self) -> bool:
#         """
#         Redis health check.
#         """

#         try:
#             return self.client.ping()

#         except Exception as ex:

#             logger.error(ex)

#             return False


import json
import logging
from typing import List, Dict

import redis

from app.config.settings import settings

logger = logging.getLogger(__name__)


class MemoryService:

    def __init__(self):

        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            username="default",
            password=settings.REDIS_PASSWORD,
            db=0,
            decode_responses=True,
        )

        logger.info("Redis connected successfully.")

    # --------------------------------------------

    def _get_key(self, session_id: str) -> str:

        return f"chat:{session_id}"

    # --------------------------------------------

    def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> None:

        key = self._get_key(session_id)

        message = {
            "role": role,
            "content": content,
        }

        self.client.rpush(
            key,
            json.dumps(message),
        )

        self.client.expire(
            key,
            3600,
        )

    # --------------------------------------------

    def save_conversation(
        self,
        session_id: str,
        messages: List[Dict],
    ) -> None:

        if not messages:
            return

        key = self._get_key(session_id)

        values = [
            json.dumps(msg)
            for msg in messages
        ]

        self.client.rpush(
            key,
            *values,
        )

        self.client.expire(
            key,
            3600,
        )

    # --------------------------------------------

    def load_history(
        self,
        session_id: str,
    ) -> List[Dict]:

        key = self._get_key(session_id)

        history = self.client.lrange(
            key,
            0,
            -1,
        )

        return [
            json.loads(item)
            for item in history
        ]

    # --------------------------------------------

    def get_last_messages(
        self,
        session_id: str,
        limit: int = 10,
    ) -> List[Dict]:

        key = self._get_key(session_id)

        history = self.client.lrange(
            key,
            -limit,
            -1,
        )

        return [
            json.loads(item)
            for item in history
        ]

    # --------------------------------------------

    def clear_history(
        self,
        session_id: str,
    ) -> None:

        self.client.delete(
            self._get_key(session_id)
        )

    # --------------------------------------------

    def session_exists(
        self,
        session_id: str,
    ) -> bool:

        return bool(
            self.client.exists(
                self._get_key(session_id)
            )
        )

    # --------------------------------------------

    def ping(self) -> bool:

        try:
            return self.client.ping()

        except Exception as ex:

            logger.error(ex)

            return False