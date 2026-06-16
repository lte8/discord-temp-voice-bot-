from dataclasses import dataclass
from dotenv import dotenv_values


@dataclass
class Config:
    """
    This class is used to store the bot's configuration.
    You can load it from a dictionary or from a .env file (recommended).
    By default in this Discord bot template, we use from_env classmethod.
    """
    discord_token: str
    discord_prefix: str
    discord_owner_id: int
    discord_join_message: str

    discord_activity_name: str
    discord_activity_type: str
    discord_status_type: str

    @classmethod
    def from_dict(self, **kwargs) -> "Config":
        """ Create a Config object from a dictionary. """
        kwargs_overwrite = {}

        for k, v in kwargs.items():
            new_key = k.lower()

            if v.isdigit():
                kwargs_overwrite[new_key] = int(v)
            else:
                kwargs_overwrite[new_key] = v

        return Config(**kwargs_overwrite)

    @classmethod
    def from_env(self, filename: str = ".env") -> "Config":
        """Create a Config object from a .env file.

        Raises:
            ValueError: if any required variables are missing (or empty).
        """
        raw = dotenv_values(filename)

        required = [
            "discord_token",
            "discord_prefix",
            "discord_owner_id",
            "discord_join_message",
            "discord_activity_name",
            "discord_activity_type",
            "discord_status_type",
        ]

        missing = [k for k in required if not raw.get(k) and not raw.get(k.upper())]
        if missing:
            # dotenv_values returns keys exactly as defined in the env file, so we check both lower/upper
            raise ValueError(
                "Missing required environment variables in "
                f"{filename}: {', '.join(missing)}. "
                "Create/complete .env based on .env.example."
            )

        # Normalize keys to lower-case for Config.from_dict
        normalized = {}
        for k, v in raw.items():
            if k is None:
                continue
            normalized[str(k).lower()] = v

        return Config.from_dict(**normalized)

