from pydantic import Field
from pydantic_settings import SettingsConfigDict

from .base import BaseSettings


class BrokerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="broker_")

    url: str = Field(default="nats://broker:4222", title="Broker URL")
    default_queue: str = Field(default="default", title="Default queue")


broker_settings = BrokerSettings()
