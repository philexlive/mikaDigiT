from typing import Any, Optional

from pydantic import BaseModel, Field

from pydantic_settings import BaseSettings, YamlConfigSettingsSource


class ChatInfo(BaseModel):
    label: str
    head_admin: str = Field(validation_alias='head-admin')
    admins: Optional[list[str]] = Field({})


class ServiceSettings(BaseSettings):
    chats: dict[int, ChatInfo]

    @classmethod
    def settings_customise_sources(
        cls, 
        settings_cls, 
        init_settings, 
        env_settings, 
        dotenv_settings, 
        file_secret_settings
    ):
        yaml_config_settings_source = YamlConfigSettingsSource(
            settings_cls, 
            yaml_file='config/service.yaml',
            yaml_file_encoding='utf-8'
        )
        return (
            init_settings, 
            env_settings, 
            dotenv_settings,
            yaml_config_settings_source, 
            file_secret_settings
        )


service_settings = ServiceSettings()