# MikaMakiLite

A simple Telegram bot using AI

# AI configuration file

In a new created file `character.yaml` inside `src/config/` directory:

```character.yaml
ai:
  model: meta-llama/Llama-3.3-70B-Instruct
  provider: groq
  who: |
    You are just a chatter in the messenger.
    Respond to:
    {}

watermark: Sample Watermark
```

# Environment variables

Sensitive info add into the top level `.env` file.
```.env
TG_API_ID=telegram_api_id
TG_API_HASH=telegram_api_hash
TG_SESSION=telegram_session_name
HF_API_KEY=huggingface_api_key
CHAT_ID=chat_you_want_to_read
```