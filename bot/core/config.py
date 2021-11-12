import re

from pydantic import BaseSettings, validator


class Client(BaseSettings):
    """The API settings."""

    name: str = "Bot"
    token: str

    @validator("token")
    def check_token_format(cls, v: str) -> str:
        """Validate discord tokens format."""
        pattern = re.compile(r"\w{24}\.\w{6}\.\w{27}")
        assert pattern.fullmatch(v), f"Discord token must follow >> {pattern.pattern} << pattern."
        return v

    class Config:
        """The Pydantic settings configuration."""

        env_file = ".env"
        env_prefix = "BOT_"


class Roles(BaseSettings):
    """The roles settings."""

    everyone: str = "@everyone"
    admin: str = everyone

    class Config:
        """The Pydantic settings configuration."""

        env_file = ".env"
        env_prefix = "ROLE_"


class Global(BaseSettings):
    """The app settings."""

    client: Client = Client()
    dev_guild_ids: list[int] = []
    guild_ids: list[int]

    roles: Roles = Roles()

    debug: bool = False

    @validator("guild_ids", "dev_guild_ids")
    def check_ids_format(cls, v: list[int]) -> list[int]:
        """Validate discord ids format."""
        for discord_id in v:
            assert len(str(discord_id)) == 18, "Discord ids must have a length of 18."
        return v

    class Config:
        """The Pydantic settings configuration."""

        env_file = ".env"


settings = Global()
