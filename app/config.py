from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str
    db_user: str
    db_password: str
    db_name: str
    source_table: str
    destination_table: str

    class Config:
        env_file = ".env"

settings = Settings()
