from typing import Optional, Self

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ClientSettings(BaseSettings):
    api_id: str = Field(validation_alias="API_ID")
    api_hash: str = Field(validation_alias="API_HASH")
    session: str = Field(validation_alias="SESSION_NAME")
    wt: str = Field(validation_alias="WATERMARK")


client_settings = ClientSettings()
