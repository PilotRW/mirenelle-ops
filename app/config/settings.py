from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ALEMBIC_DATABASE_URL: str
    OA_DATABASE_URL: str | None = None
    AMAZON_SP_API_REFRESH_TOKEN: str | None = None
    AMAZON_SP_API_LWA_CLIENT_ID: str | None = None
    AMAZON_SP_API_LWA_CLIENT_SECRET: str | None = None
    AMAZON_SP_API_AWS_ACCESS_KEY: str | None = None
    AMAZON_SP_API_AWS_SECRET_KEY: str | None = None
    AMAZON_SP_API_AWS_ROLE_ARN: str | None = None
    AMAZON_SP_API_REGION: str = "eu-west-1"
    AMAZON_SP_API_ENDPOINT: str = "https://sellingpartnerapi-eu.amazon.com"

    AUTH_ENABLED: bool = False
    AUTH_SESSION_SECRET: str = "dev-insecure-session-secret"
    AUTH_ISSUER: str | None = None
    AUTH_CLIENT_ID: str | None = None
    AUTH_CLIENT_SECRET: str | None = None
    AUTH_REDIRECT_URI: str | None = None
    AUTH_GROUPS_CLAIM: str = "groups"
    AUTH_DEV_USER: str = "dev@mirenelle.local"
    AUTH_DEV_ROLES: str = "owner"

    class Config:
        env_file = ".env"


settings = Settings()
