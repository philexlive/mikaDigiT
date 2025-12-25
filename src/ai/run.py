from typing import Union

from fastapi import FastAPI

from src.services.ai_service import ClientResponse, TextRequest, AIService


app = FastAPI()

@app.put("/process")
async def process_ai(request: TextRequest):
    # service = await AIService(
    #     ai='huggingface'
    #     model='meta-llama/Llama-3.3-70B-Instruct'
    # )
    service = AIService(
        ai='mistral',
        model='mistral-medium-latest'
    )
    return await service.run(request)
