from datetime import UTC, datetime
from typing import Any
from urllib.parse import urljoin

import httpx
import taskiq_fastapi
from taskiq import TaskiqMessage, TaskiqMiddleware, TaskiqResult
from taskiq_nats import NatsBroker
from taskiq_redis import RedisAsyncResultBackend

from settings import broker_settings, redis_settings


class TaskiqAdminMiddleware(TaskiqMiddleware):
    def __init__(
        self,
        url: str,
        api_token: str,
        taskiq_broker_name: str | None = None,
    ):
        super().__init__()
        self.url = url
        self.api_token = api_token
        self.__ta_broker_name = taskiq_broker_name

    async def post_send(self, message) -> Any:
        now = datetime.now(UTC).replace(tzinfo=None).isoformat()
        async with httpx.AsyncClient() as client:
            await client.post(
                headers={"access-token": self.api_token},
                url=urljoin(self.url, f"/api/tasks/{message.task_id}/queued"),
                json={
                    "args": message.args,
                    "kwargs": message.kwargs,
                    "taskName": message.task_name,
                    "worker": self.__ta_broker_name,
                    "queuedAt": now,
                },
            )
        return super().post_send(message)

    async def pre_execute(self, message: TaskiqMessage) -> Any:
        now = datetime.now(UTC).replace(tzinfo=None).isoformat()
        async with httpx.AsyncClient() as client:
            await client.post(
                headers={"access-token": self.api_token},
                url=urljoin(self.url, f"/api/tasks/{message.task_id}/started"),
                json={
                    "startedAt": now,
                    "args": message.args,
                    "kwargs": message.kwargs,
                    "taskName": message.task_name,
                    "worker": self.__ta_broker_name,
                },
            )
        return super().pre_execute(message)

    async def post_execute(
        self,
        message: TaskiqMessage,
        result: TaskiqResult[Any],
    ) -> Any:
        now = datetime.now(UTC).replace(tzinfo=None).isoformat()
        async with httpx.AsyncClient() as client:
            await client.post(
                headers={"access-token": self.api_token},
                url=urljoin(
                    self.url,
                    f"/api/tasks/{message.task_id}/executed",
                ),
                json={
                    "finishedAt": now,
                    "error": (
                        result.error if result.error is None else repr(result.error)
                    ),
                    "executionTime": result.execution_time,
                    "returnValue": {"return_value": result.return_value},
                },
            )
        return super().post_execute(message, result)


broker = (
    NatsBroker(servers=broker_settings.url, queue=broker_settings.default_queue)
    .with_result_backend(
        result_backend=RedisAsyncResultBackend(redis_url=redis_settings.url),
    )
    .with_middlewares(
        TaskiqAdminMiddleware(
            url=broker_settings.ui_url,
            api_token=broker_settings.api_token,
            taskiq_broker_name=broker_settings.name,
        )
    )
)


taskiq_fastapi.init(broker=broker, app_or_path="main:app")
