from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from loguru import logger

from api.configs.clickhouse.database_click import database as clickhouse, engine
from api.db_models.clickhouse.model import Log as LogModel

router = APIRouter()


class LogCreate(BaseModel):
    timestamp: datetime
    source: str
    level: str
    message: str


class Log(LogCreate):
    id: int


@router.post("/logs")
async def create_log(log: LogCreate) -> dict:
    logger.info(f"Creating log: {log}")
    await clickhouse.client.insert(
        "logs",
        [[log.timestamp, log.source, log.level, log.message]],
        column_names=["timestamp", "source", "level", "message"],
    )
    logger.info(f"Log created successfully")
    return {"status": "success"}


@router.get("/logs")
async def get_all_logs() -> list[LogCreate]:
    logger.info(f"Getting all logs")
    query = str(select(LogModel).order_by(LogModel.timestamp.desc()).compile(engine))
    rows = await clickhouse.fetch_all(query)
    logger.info(f"Logs fetched successfully: {rows}")
    return [
        LogCreate(timestamp=t, source=s, level=l, message=m)
        for t, s, l, m in rows
    ]
