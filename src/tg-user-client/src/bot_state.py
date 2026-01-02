import os

from typing import Literal, Self

from pydantic import BaseModel


class ChatState(BaseModel):
    label: str
    id: int
    active: bool = False


class BotState(BaseModel):
    active: bool = False
    chats: list[ChatState] = []


class StateManager:
    def __init__(self, filename: str = "var/state.json"):
        self.filename = filename
        self.state = self.load()

    def load(self) -> BotState:
        if not os.path.isdir('var'):
            os.mkdir('var')
            
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return BotState.model_validate_json(f.read())
        
        return self.get_default_states('off')
    
    def save(self):
        with open(self.filename, 'w') as f:
            f.write(self.state.model_dump_json(indent=4))
    
    @staticmethod
    def get_default_states(mode: Literal['on', 'off']) -> BotState:
        match mode:
            case 'on': return BotState(active=True)
            case _: return BotState()