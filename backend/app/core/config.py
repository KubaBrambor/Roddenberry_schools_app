from pathlib import Path

from pydantic import PostgresDsn, TypeAdapter, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    # PostgresDsn represents a standardized PostgreSQL connection string
    DATABASE_URI: PostgresDsn | None = None

    @field_validator("DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(
        cls, v: PostgresDsn | str | None, info: ValidationInfo
    ) -> PostgresDsn:
        # If already a PostgresDsn, return it
        if isinstance(v, PostgresDsn):
            return v

        if isinstance(v, str):
            # Use TypeAdapter to validate and convert string to PostgresDsn
            return TypeAdapter(PostgresDsn).validate_python(v)

        # Extract values from the model
        values = info.data

        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=values.get("POSTGRES_DB"),
        )

    # Conversion method for SQLAlchemy
    def get_connection_string(self) -> str:
        # Convert PostgresDsn to string for create_engine
        if self.DATABASE_URI:
            return str(self.DATABASE_URI)
        raise ValueError("Database URI not configured")

    model_config: SettingsConfigDict = SettingsConfigDict(  # pyright: ignore[reportIncompatibleVariableOverride]
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
