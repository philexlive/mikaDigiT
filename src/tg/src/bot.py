import httpx

from telethon import TelegramClient, events

from src.config.client_settings import settings


client = TelegramClient(
    session=settings.session, 
    api_id=settings.api_id, 
    api_hash=settings.api_hash
)


@client.on(events.NewMessage)
async def replies(event):
    msg = event.raw_text
    if 'mika' in msg and event.chat_id == settings.chat_id:
        async with httpx.AsyncClient() as http_client:
            sender = await event.get_sender()
            message = "{} {} (usrname: {}): {}".format(
                sender.first_name,
                sender.last_name,
                sender.username,
                event.message
            )

            response = await http_client.put(
                'http://127.0.0.1:8000/process',
                json={'text': message}
            )
            response = response.json()
            await event.reply(response['text'] + '\n🍭 **mikaDidiT**')

client.start()
client.loop.run_forever()