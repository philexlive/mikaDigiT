import os
import dotenv
import yaml


dotenv.load_dotenv()


class TgConfig:
    api_id = os.getenv("TG_API_ID")
    api_hash = os.getenv("TG_API_HASH")
    session = os.getenv("TG_SESSION")


class CharacterConfig:
    class AIInfo:
        api_key: str = os.getenv("HF_API_KEY")
        
        def __init__(self, model, provider, who):
            self.model: str = model
            self.provider: str = provider
            self.who: str = who
        # model: str
        # provider: str
        # who: str

    def __init__(self):
        self.ai: CharacterConfig.AIInfo = None
        self.watermark: str = None
        try:
            with open("src/config/character.yaml") as stream:
                data = yaml.safe_load(stream)
                
                ai_conf = data["ai"]
                self.ai = CharacterConfig.AIInfo(
                    model=ai_conf["model"],
                    provider = ai_conf["provider"],
                    who = ai_conf["who"]
                )

                self.watermark = data["watermark"]
        except yaml.YAMLError as e:
            print(e)


character_config = CharacterConfig()


dotenv.load_dotenv()


CHAT_ID=int(os.getenv("CHAT_ID"))