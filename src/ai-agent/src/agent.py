from pydantic_ai import Agent, RunContext

from src.core.text_request import TextRequest
from src.core.agent_response import AgentResponse

from src.config.persona_settings import persona_settings


agent = Agent(
    output_type=AgentResponse,
    instructions='You answer user\'s responses',
    system_prompt= [
        f"Your name: {persona_settings.persona.name}",
        persona_settings.persona.bio,
    ],
    end_strategy='exhaustive',
)


@agent.system_prompt
def inject_sender_info(ctx: RunContext[TextRequest]) -> str:
    r = ctx.deps
    return f"You are talking to {r.first_name} {r.second_name} ({r.username})."