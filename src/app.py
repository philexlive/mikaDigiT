import config
import asyncio
import telethon as tl

from ai.mikamakilite import client
from tbl import get_table_from_chat


def run_ai():
    with client:
        client.run_until_disconnected()


def run_reading():
    with client:
        table = get_table_from_chat(config.CHAT, config.TOPIC, client)
        asyncio.run(table)


def main():
    client.start()
    # run_reading()
    run_ai()
    if client.is_connected:
        client.disconnect()


if __name__ == "__main__":
    main()