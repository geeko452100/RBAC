from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Get the url
    DATABASE_URL: str

    # Tell pydantic to look for for an external `.env` file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Create a single global instance of the Settings Class to use anywhere
settings = Settings()