import os

from typing import Literal

from pydantic import BaseModel


class AgentState(BaseModel):
    model: Literal['huggingface', 'mistral']


class StateManager:
    filename = 'app/var/states/state.json'

    def __init__(self):
        self.state = self.load()

    def load(self):
        if not os.path.isdir('var'):
            os.mkdir('var')
        
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return AgentState.model_validate_json(f.read())
        
        return AgentState(model='huggingface')
    

    def save(self):
        with open(self.filename, 'w') as f:
            f.write(self.state.model_dump_json(indent=4))