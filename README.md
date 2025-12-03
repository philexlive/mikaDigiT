# MikaMakiLite

A simple Telegram bot using AI

# AI configuration file

In a new created file `ai.yaml` inside `src/config/` directory:

```ai.yaml
ai:
    model: meta-llama/Llama-3.3-70B-Instruct
    provider: groq
    character: |
        You are just a chatter in the messager.
        Respond to:
        {}
```