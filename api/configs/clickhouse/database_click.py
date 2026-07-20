from urllib.parse import urlparse

import clickhouse_connect
import sqlalchemy

from api.configs.clickhouse.config_clickhouse import config


def _parse_url(url: str) -> dict:
    parsed = urlparse(url)
    return {
        "host": parsed.hostname or "localhost",
        "port": parsed.port or 8123,
        "username": parsed.username or "default",
        "password": parsed.password or "",
        "database": parsed.path.lstrip("/") or "default",
    }


def _sqlalchemy_url(url: str) -> str:
    parsed = urlparse(url)
    username = parsed.username or "default"
    password = parsed.password or ""
    host = parsed.hostname or "localhost"
    port = parsed.port or 8123
    database = parsed.path.lstrip("/") or "default"
    return f"clickhouse://{username}:{password}@{host}:{port}/{database}"


class ClickHouseDatabase:
    def __init__(self, url: str | None):
        self._url = url
        self._client = None

    async def connect(self) -> None:
        self._client = await clickhouse_connect.get_async_client(
            **_parse_url(self._url)
        )

    async def disconnect(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None

    async def fetch_all(self, query: str, values: dict | None = None):
        result = await self._client.query(query, parameters=values)
        return result.result_rows

    async def fetch_one(self, query: str, values: dict | None = None):
        rows = await self.fetch_all(query, values)
        return rows[0] if rows else None

    async def execute(self, query: str, values: dict | None = None):
        await self._client.command(query, parameters=values)

    @property
    def client(self):
        return self._client


database = ClickHouseDatabase(config.CLICKHOUSE_URL)

engine = sqlalchemy.create_engine(_sqlalchemy_url(config.CLICKHOUSE_URL))

from api.db_models.clickhouse.model import Base  # noqa: E402

Base.metadata.create_all(engine)
