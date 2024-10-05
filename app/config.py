from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_password: str
    source_table: str
    source_column_name: str
    destination_table: str
    destination_column_name: str

    class Config:
        env_file = "env/.env"

settings = Settings()
