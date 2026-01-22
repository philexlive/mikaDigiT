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
logging.basicConfig(level=logging.INFO)


@app.post("/process")
async def process_ai(request: TextRequest) -> AgentResponse:
    if request.behaviour in persona_settings.behaviours:
        logger.info(f"Conversation has {request.behaviour} behaviour.")

        behaviour = persona_settings.behaviours[request.behaviour]
    else:
        logger.info(f"Conversation has no {request.behaviour} behaviour.")
        
        behaviour = None
    
    model = agent_settings.models[state_manager.load().model]

    response = await agent.run(
        request.text,
        model=model,
        instructions=behaviour,
        deps=request,
    )

    logger.info(f"Response {response}")
    return response.output


@app.post("/state")
async def set_agent_model(state: AgentState):
    state_manager.state = state
    state_manager.save()


@app.get("/state")
async def  get_agent_state():
    return state_manager.state