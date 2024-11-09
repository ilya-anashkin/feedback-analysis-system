from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    The Settings class is used to load and validate the application configuration
    from environment variables or a `.env` file.

    Attributes:
        db_host (str): The database host.
        db_port (str): The port to connect to the database.
        db_name (str): The name of the database.
        db_user (str): The username for connecting to the database.
        db_password (str): The password for the database user.
        source_table (str): The name of the source table in the database.
        source_column_name (str): The name of the source column in the source table.
        destination_table (str): The name of the destination table in the database.
        destination_column_name (str): The name of the destination column in the destination table.

    Nested classes:
        Config:
            Contains configuration options for the Settings class.
            Specifies the `env/.env` file for loading environment variables.
    """

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
        """
        The Config class is used to define configuration options.

        Attributes:
            env_file (str): Path to the `.env` file that contains environment variables.
        """

        env_file = "env/.env"


settings = Settings()
