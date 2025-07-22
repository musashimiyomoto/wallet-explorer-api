from pydantic import Field

from .base import BaseSettings


class ExplorerSettings(BaseSettings):
    tron_api_key: str | None = Field(default=None, title="Tron API key")


explorer_settings = ExplorerSettings()
