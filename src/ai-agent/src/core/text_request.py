from typing import Optional

from pydantic import BaseModel, Field

class TextRequest(BaseModel):
    label: str = Field(description='Label of the chat')
    first_name: str = Field(description='First name of the sender')
    second_name: str = Field(description='Second name of the sender')
    username: Optional[str] = Field(None, description='Unique username of the sender')
    text: str = Field(description='The message of the sender')