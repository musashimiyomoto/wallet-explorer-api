from pydantic import Field

from .base import BaseSettings


class ExplorerSettings(BaseSettings):
    tron_api_key: str = Field(default=..., title="Tron API key")


explorer_settings = ExplorerSettings()
