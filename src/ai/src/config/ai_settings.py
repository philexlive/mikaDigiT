from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Provides environmental variable for an ai service
class AISettings(BaseSettings):
    model_name: str = Field(validation_alias="MODEL")
    provider_name: Optional[str] = Field(None, validation_alias="PROVIDER")
    base_url: Optional[str] = Field(None, validation_alias="BASE_URL")
    hf_api_key: Optional[str] = Field(None, validation_alias="HF_TOKEN")
    mistral_api_key: Optional[str] = Field(None, validation_alias="MISTRAL_API_KEY")

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra='ignore')


ai_settings = AISettings()