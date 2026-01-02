from typing import Optional

from pydantic import BaseModel

from pydantic_settings import (
    BaseSettings,
    YamlConfigSettingsSource
)


class Persona(BaseModel):
    name: str = "Chatter"
    bio: str = "You are just a chatter"

class PersonaSettings(BaseSettings):
    persona: Persona = Persona()
    labels: dict[str, Optional[str]] = {}

    @classmethod
    def settings_customise_sources(
        cls, 
        settings_cls, 
        init_settings, 
        env_settings, 
        dotenv_settings, 
        file_secret_settings
    ):
        return (
            init_settings, 
            env_settings, 
            dotenv_settings, 
            YamlConfigSettingsSource(
                settings_cls, 
                yaml_file='config/persona.yaml',
                yaml_file_encoding='utf-8'
            ),
            file_secret_settings
        )


persona_settings = PersonaSettings()