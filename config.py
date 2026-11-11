# import os
# from pydantic_settings import BaseSettings, SettingsConfigDict

# class Settings(BaseSettings):
#     TELEGRAM_BOT_TOKEN: str
#     GEMINI_API_KEY: str

#     model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# settings = Settings()



# from pydantic_settings import BaseSettings, SettingsConfigDict

# class Settings(BaseSettings):
#     TELEGRAM_BOT_TOKEN: str
#     GEMINI_API_KEY: str
#     ADMIN_PASSWORD: str = "secure_default_password"
#     SECRET_KEY: str = "super_secret_session_key"

#     model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# settings = Settings()


from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    GEMINI_API_KEY: str  # This automatically matches GEMINI_API_KEY from your .env file
    ADMIN_PASSWORD: str = "admin123"
    SECRET_KEY: str = "session_secret"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()