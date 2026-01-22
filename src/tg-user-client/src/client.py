import logging

import httpx

from typing import Any

from telethon import TelegramClient, events, types

from src.config.client_settings import client_settings
from src.config.service_settings import service_settings
from src.bot_state import StateManager, BotState, ChatState


URL = 'http://app:8000/tg-user-client-event'


client = TelegramClient(
    session=f"/app/sessions/{client_settings.session}.session", 
    api_id=client_settings.api_id, 
    api_hash=client_settings.api_hash
)


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
logging.basicConfig(filename='var/output.txt', level=logging.INFO)


state_manager = StateManager()


async def get_response(
    label: str,
    first_name: str,
    second_name: str,
    username: str,
    text: str
) -> str:
    async with httpx.AsyncClient() as http_client:
        try:
            request = {
                'label': label,
                'first_name': first_name,
                'second_name': second_name or "",
                'username': username,
                'text': text
            }
            logger.info(f"request: {request}")
            response = await http_client.post(URL, json=request)
            logger.info(f"response: {response}")
            response = response.json()['text']
        except httpx.RequestError as e:
            logger.error(e)
            response = "Sry, bad request to AI..."
        
        return f"{response}\n{client_settings.wt}"


def set_chat_active_by_id(
    chat_id: int, 
    value: bool = False, 
    state_manager: StateManager = state_manager
) -> BotState:
    for (id, chat) in service_settings.chats.items():
        if chat_id == id:
            break
    else:
        return
    
    try:
        chat = next((c for c in state_manager.state.chats if c.id == chat_id))
    except:
        chat = None
    
    if chat:
        chat.active = value
    else:
        chat = ChatState(
            label=service_settings.chats[chat_id].label, 
            id=chat_id,
            active=value
        )
        state_manager.state.chats.append(chat)

    state_manager.save()
    logger.info(state_manager.state)
            


def set_chat_active_by_label(label: str, value: bool):
    for chat in state_manager.state.chats:
        if chat.label == label:
            logger.info(f"{chat.label} set to {False}")
            chat.active = value
            state_manager.save()
            break
    return state_manager.state


def check_chat_active() -> bool:
    logger.info(state_manager.state.chats)


def check_sender_anonymous(event) -> bool:
    is_anonymous = False
    if not event.from_id:
        is_anonymous = True
    elif isinstance(event.from_id, types.PeerChannel):
        if event.sender_id == event.chat_id:
            is_anonymous = True
    
    return is_anonymous


async def response(event) -> dict[str, Any]:
    sender = await event.get_sender()
    # Responding
    username = f'@{sender.username}' if sender.username else ''
    response = await get_response(
        label=service_settings.chats[event.chat_id].label,
        first_name=sender.first_name,
        second_name=sender.last_name,
        username=username,
        text=event.message.text
    )

    return await event.reply(response)


async def user_handler(event):
    chat_id = event.chat_id
    try:
        available = next((c.active for c in state_manager.state.chats if c.id == chat_id))
    except:
        available = False

    if not available:
        return
    
    logger.info("Responding")

    sender = await event.get_sender()
    response = await get_response(
        label=service_settings.chats[chat_id].label,
        first_name=sender.first_name,
        second_name=sender.last_name,
        username=sender.username,
        text=event.message.text
    )
    await event.reply(response)
    
    logger.info("User")


async def anonymous_admin_handler(event):
    logger.info("Anonymous Admin")
    
    chat_id = event.chat_id
    msg = event.message.text
    if msg == 'mika сладкое': # TODO Replace with your command
        set_chat_active_by_id(chat_id, True)
    elif msg == 'mika душнишь': # TODO Replace with your command
        set_chat_active_by_id(chat_id)
    else:
        chat = await event.get_chat()
        response = await get_response(
            label=service_settings.chats[chat_id].label,
            first_name=chat.title,
            second_name='',
            username='',
            text=event.message.text
        )
        await event.reply(response)


async def admin_handler(event):
    logger.info("Admin")

    chat_id = event.chat_id
    msg = event.message.text
    if msg == 'mika сладкое': # TODO Replace with your command
        set_chat_active_by_id(chat_id, True)
    elif msg == 'mika душнишь': # TODO Replace with your command
        set_chat_active_by_id(chat_id)
    else:
        await user_handler(event)


@client.on(events.NewMessage)
async def handler(event):
    check_chat_active()
    if not 'mika' in event.message.text: # TODO Replace with your command
        logger.info('Conversation has no keyword.')
        return
    
    if not state_manager.state.active:
        logger.info('Chat inactive.')
        return

    if not event.chat_id in service_settings.chats:
        logger.info('Not included to conf user trying to access the bot.')
        return
    logger.info('Conversation starting...')

    is_sender_anonymous = check_sender_anonymous(event)
    if is_sender_anonymous:
        await anonymous_admin_handler(event)
    else:
        sender = await event.get_sender()

        if isinstance(event.from_id, types.Channel):
            logger.info("Chat")
            await anonymous_admin_handler(event)
            return
        
        chat_conf = service_settings.chats[event.chat_id]
        username = sender.username

        
        if username == chat_conf.head_admin or username in chat_conf.admins:
            await admin_handler(event)
        else:
            await user_handler(event)