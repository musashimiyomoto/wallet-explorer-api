from pydantic import Field
from pydantic_settings import SettingsConfigDict

from .base import BaseSettings


class BrokerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="broker_")

    name: str = Field(default="explorer", title="Broker Name")
    url: str = Field(default="nats://broker:4222", title="Broker URL")
    ui_url: str = Field(default="http://broker-ui:3000", title="Broker URL")
    default_queue: str = Field(default="default", title="Default queue")
    api_token: str = Field(default=..., title="API Token")


broker_settings = BrokerSettings()
