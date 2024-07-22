from pydantic import BaseSettings

class Settings(BaseSettings):
    AZURE_SPEECH_KEY: str
    AZURE_SPEECH_REGION: str
    AZURE_SOURCE_LANG_CODE: str
    AZURE_OAI_KEY: str
    AZURE_OAI_DEPLOYMENT: str
    AZURE_OAI_ENDPOINT: str
    AZURE_SPEECH_ID_EN: str
    AZURE_SPEECH_ID_TR: str
    AZURE_OAI_WHISPER_KEY: str
    AZURE_OAI_WHISPER_REGION: str
    AZURE_OAI_WHISPER_ENDPOINT: str
    AZURE_OAI_WHISPER_DEPLOYMENT: str
    AZURE_OAI_TTS_KEY: str
    AZURE_OAI_TTS_ENDPOINT: str
    AZURE_T2S_SPEECH_KEY: str
    THY_API_KEY: str
    THY_API_SECRET: str
    CUSTOM_MODAL: str
    DATABASE_SERVER: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    # DATABASE_URL: str = "sqlite:///./test.db"

with open ("config.json", "r") as f:
    config = json.load(f)
settings = Settings(**config)