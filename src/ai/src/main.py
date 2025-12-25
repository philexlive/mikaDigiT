import asyncio

from src.services.ai_service import AIService

async def main():
    # service = AIService('huggingface', model='meta-llama/Llama-3.3-70B-Instruct')
    service = AIService('mistral')
    await service.run()
 
if __name__ == "__main__":
    asyncio.run(main())