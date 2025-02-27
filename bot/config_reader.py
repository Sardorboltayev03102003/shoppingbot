from pydantic import  SecretStr, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings, extra= 'allow'):
    bot_token: SecretStr
    db_url: str
    pgadmin_user: str
    pgadmin_password: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")



config = Settings()
