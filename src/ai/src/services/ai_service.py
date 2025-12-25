from typing import Literal, Optional

from pydantic import BaseModel, Field

from pydantic_ai import Agent

from src.config.persona import persona
from src.config.ai_settings import ai_settings

from src.core.ai_source import AISource

from src.sources.huggingface_source import HuggingFaceSource
from src.sources.mistral_source import MistralSource


# Text response of model
class ClientResponse(BaseModel):
    text: str = Field(description="Client responded.")


class TextRequest(BaseModel):
    text: str = Field(description="Other user message")


class AIService:
    def __init__(
        self, ai: Literal['mistral', 'huggingface'], 
        model: Optional[str] = None
    ):
        self.ai = ai
        self.model=model

    async def run(self, request: TextRequest) -> ClientResponse:
        source: AISource
        
        settings = ai_settings
        if not self.model == None:
            settings = ai_settings.model_copy(update={'model_name': self.model})
        settings = settings.model_dump(exclude_none=True)


        print(settings)


        match self.ai:
            case 'mistral':
                source = MistralSource(**settings)
            case 'huggingface':
                source = HuggingFaceSource(**settings)

        model = source.build()

        instructions=(
            'Your name: {name}'
            'Your bio:'
            '{bio}'
        ).format(
            name=persona.name,
            bio=persona.bio
        )
        ai_client = Agent(
            model,
            output_type=ClientResponse,
            instructions=instructions,
            end_strategy='exhaustive'
        )

        result = await ai_client.run(request.text)
        
        return result.output