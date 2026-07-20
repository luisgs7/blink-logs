from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.configs.postgresql.database_pg import database
from api.configs.clickhouse.database_click import database as clickhouse

from api.routes.logs import router as logs_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    await clickhouse.connect()
    yield
    await clickhouse.disconnect()
    await database.disconnect()

app = FastAPI(title="BlinkLogs", lifespan=lifespan)


@app.get("/ping")
def ping():
    return {"status": "online ;)"} 
 
app.include_router(logs_router)