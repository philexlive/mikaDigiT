from pydantic import BaseModel, Field

class AgentResponse(BaseModel):
    text: str = Field(description='Agent responce')