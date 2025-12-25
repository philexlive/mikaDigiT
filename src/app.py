from typing import Union
# from fastapi import FastAPI
from src.tg.bot import client

# app = FastAPI()


def run_ai():
    with client:
        client.run_until_disconnected()


def main():
    client.start()
    run_ai()
    if client.is_connected:
        client.disconnect()


if __name__ == "__main__":
    main()