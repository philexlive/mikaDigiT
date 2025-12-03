from .config import TgConfig, ai_config
from telethon import TelegramClient, events
from huggingface_hub import InferenceClient


inference = InferenceClient(
    model=ai_config.model, 
    provider=ai_config.provider, 
    api_key=ai_config.api_key
)
client = TelegramClient(
    TgConfig.session, 
    TgConfig.api_id, 
    TgConfig.api_hash
)


@client.on(events.NewMessage)
async def my_event_handler(event):
    msg = event.raw_text
    if 'MikaMakiLite' in msg:
        completion = inference.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": ai_config.character.format(msg)
                }
            ]
        )
        await event.reply(completion.choices[0].message.content + "\n\n🍭 MikaMakiLite")
