import httpx

from fastapi import FastAPI


URL = 'http://ai-agent:8000/process'


app = FastAPI()


@app.put('/tg-user-bot-event')
async def get_ai_response(message: dict) -> dict:
    response = await httpx.put(URL, json=message)
    response = response.json()
    return response