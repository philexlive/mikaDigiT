from typing import Union

from fastapi import FastAPI

from src.services.ai_service import ClientResponse, TextRequest, AIService


app = FastAPI()

@app.put("/process")
async def process_ai(request: TextRequest):
    service = await AIService(ai='mistral').run(request)
    return service
