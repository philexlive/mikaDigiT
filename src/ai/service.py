from config import TgConfig, character_config, CHAT_ID
from telethon import TelegramClient, events
from huggingface_hub import InferenceClient


inference = InferenceClient(
    model=character_config.ai.model, 
    provider=character_config.ai.provider, 
    api_key=character_config.ai.api_key
)
client = TelegramClient(
    session=TgConfig.session, 
    api_id=TgConfig.api_id, 
    api_hash=TgConfig.api_hash
)


@client.on(events.NewMessage)
async def replies(event):
    msg = event.raw_text
    if 'MikaMakiLite' in msg and event.chat_id == CHAT_ID:
        completion = inference.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": character_config.ai.who.format(msg)
                }
            ]
        )
        reply = "{}\n\n{}".format(
            completion.choices[0].message.content,
            character_config.watermark
        )
        await event.reply(reply)
