import httpx

from fastapi import FastAPI


URL = 'http://ai-agent:8000/process'


app = FastAPI()


@app.post('/tg-user-client-event')
async def get_ai_response(message: dict) -> dict:
    async with httpx.AsyncClient() as httpx_client:
        response = await httpx_client.post(URL, json=message)
        response = response.json()
        return response