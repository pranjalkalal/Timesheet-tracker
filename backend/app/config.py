import os


class Settings:
    """Application settings loaded from environment variables."""

    # JWT configuration
    JWT_SECRET: str = os.getenv("JWT_SECRET", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_MINUTES: int = int(os.getenv("JWT_EXPIRATION_MINUTES", "30"))

    # Database configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

    # Application configuration
    APP_NAME: str = "Timesheet Tracker"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    def __init__(self):
        """Validate required settings."""
        if not self.JWT_SECRET:
            raise ValueError(
                "JWT_SECRET environment variable is required but not set. "
                "Please set it before starting the application."
            )

    def __repr__(self) -> str:
        return (
            f"Settings(app={self.APP_NAME}, db={self.DATABASE_URL}, "
            f"jwt_alg={self.JWT_ALGORITHM}, debug={self.DEBUG})"
        )


# Singleton settings instance
settings = Settings()
