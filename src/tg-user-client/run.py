import asyncio
import configparser

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.client import client, state_manager
from src.config.service_settings import service_settings


app = FastAPI()

config = configparser.ConfigParser()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await client.connect()

    client_task = asyncio.create_task(client.run_until_disconnected())

    yield

    await client.disconnect()
    client_task.cancel()


app.router.lifespan_context = lifespan


@app.get("/bot/state")
async def get_bot_state():
    return state_manager.state


@app.get("/bot/conf")
async def get_bot_conf():
    return service_settings.chats


@app.put("/bot/state")
async def toggle_bot():
    if state_manager.state.active:
        state_manager.state.active = False
    else:
        state_manager.state.active = True
    
    state_manager.save()
    return state_manager.state.active

