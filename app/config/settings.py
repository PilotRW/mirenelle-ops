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

    class Config:
        env_file = ".env"


settings = Settings()
