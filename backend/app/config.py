import ssl
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from pydantic_settings import BaseSettings, SettingsConfigDict


def _to_asyncpg_url(url: str) -> str:
    url = url.strip()
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://") :]
    if url.startswith("postgresql://"):
        url = "postgresql+asyncpg://" + url[len("postgresql://") :]

    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    for key in ("sslmode", "ssl", "channel_binding"):
        query.pop(key, None)
    return urlunparse(parsed._replace(query=urlencode(query)))


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/darukaa"
    JWT_SECRET: str = "supersecretkey"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    FRONTEND_URL: str = "http://localhost:5173"
    MAPBOX_TOKEN: str = ""
    COOKIE_SECURE: bool = False

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def async_database_url(self) -> str:
        return _to_asyncpg_url(self.DATABASE_URL)

    @property
    def database_connect_args(self) -> dict:
        parsed = urlparse(
            self.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
        )
        host = (parsed.hostname or "").lower()
        query = dict(parse_qsl(parsed.query, keep_blank_values=True))
        sslmode = query.get("sslmode", "").lower()
        needs_ssl = "render.com" in host or sslmode in {
            "require",
            "verify-ca",
            "verify-full",
        }
        if not needs_ssl:
            return {}
        ctx = ssl.create_default_context()
        if sslmode in {"require", ""}:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        return {"ssl": ctx}

    @property
    def cors_origins(self) -> list[str]:
        origins = [
            origin.strip().rstrip("/")
            for origin in self.FRONTEND_URL.split(",")
            if origin.strip()
        ]
        extras = [
            "https://darukaa-earth-frontend-dkmb.onrender.com",
            "http://localhost:5173",
        ]
        for origin in extras:
            if origin not in origins:
                origins.append(origin)
        return origins


settings = Settings()
