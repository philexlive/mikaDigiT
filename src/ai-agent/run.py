import logging

from typing import Literal

from fastapi import FastAPI

from src.core.text_request import TextRequest
from src.core.agent_response import AgentResponse

from src.agent import agent

from src.config.persona_settings import persona_settings
from src.config.agent_settings import agent_settings

from src.agent_state import StateManager
from src.agent_state import AgentState


app = FastAPI()
state_manager = StateManager()


logger = logging.getLogger(__name__)
logging.basicConfig(filename='var/logs.txt', level=logging.INFO)


@app.put("/process")
async def process_ai(request: TextRequest) -> AgentResponse:
    if request.label in persona_settings.labels:
        logger.info(f"Conversation has {request.label} label.")

        xs = "Conversations examples (You are {name}):\n{conv}".format(
            conv=persona_settings.labels[request.label],
            name=persona_settings.persona.name
        )
    else:
        logger.info(f"Conversation has no {request.label} label.")
        xs = None
    
    match state_manager.load().model:
        case 'huggingface':
            logger.info("Hugging Face model used.")
            model = agent_settings.models.huggingface.build()
        case 'mistral':
            logger.info("Mistral model used.")
            model = agent_settings.models.mistral.build()

    response = await agent.run(
        request.text,
        model=model,
        instructions=xs,
        deps=request,
    )

    logger.info(f"Response {response}")
    return response.output


@app.post("/state")
async def set_agent_model(model: Literal['huggingface', 'mistral']):
    state_manager.state.model = model
    state_manager.save()