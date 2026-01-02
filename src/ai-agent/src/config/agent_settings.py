from typing import Optional

from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
    YamlConfigSettingsSource
)

from pydantic_ai.models import Model
from pydantic_ai.models.huggingface import HuggingFaceModel
from pydantic_ai.providers.huggingface import HuggingFaceProvider
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider


class AgentConfigBase(BaseModel):
    api_key: str
    model_name: str

    def build(self) -> Model:
        raise NotImplementedError


class HuggingFaceConf(AgentConfigBase):
    api_key: str = Field(validation_alias="api-key")
    model_name: str = Field("meta-llama/Llama-3.3-70B-Instruct",
                            validation_alias="model")
    provider: str = Field(validation_alias="provider")
    
    def build(self) -> HuggingFaceModel:
        provider = HuggingFaceProvider(
            api_key=self.api_key,
            provider_name=self.provider
        )
        model = HuggingFaceModel(
            self.model_name,
            provider=provider
        )

        return model
    


class MistralConf(AgentConfigBase):
    api_key: str = Field(validation_alias="api-key")
    model_name: str = Field("mistral-medium-latest",
                            validation_alias="model")
    
    def build(self) -> MistralModel:
        provider = MistralProvider(api_key=self.api_key)
        model = MistralModel(
            self.model_name,
            provider=provider
        )

        return model


class ModelsContainer(BaseModel):
    huggingface: HuggingFaceConf = None
    mistral: MistralConf = None


class AgentSettings(BaseSettings):
    models: ModelsContainer = ModelsContainer()
    
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
            yaml_file='config/models.yaml',
            yaml_file_encoding='utf-8'
        )
        return (
            init_settings, 
            env_settings, 
            dotenv_settings, 
            yaml_config_settings_source,
            file_secret_settings
        )
    

agent_settings = AgentSettings()