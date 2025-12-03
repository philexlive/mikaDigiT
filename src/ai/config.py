import os
import dotenv
import yaml


dotenv.load_dotenv()


class TgConfig:
    api_id = os.getenv("TG_API_ID")
    api_hash = os.getenv("TG_API_HASH")
    session = os.getenv("TG_SESSION")


class MikaMakiLiteConfig:
    api_key = os.getenv("HF_API_KEY")

    def __init__(self):    
        try:
            with open("src/config/ai.yaml") as stream:
                ai = yaml.safe_load(stream)["ai"]
                self.model = ai["model"]
                self.provider = ai["provider"]
                self.character = ai["character"]
        except yaml.YAMLError as e:
            print(e)


ai_config = MikaMakiLiteConfig()
