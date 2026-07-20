import databases
import sqlalchemy
from api.configs.postgresql.config_postgresql import config

metadata = sqlalchemy.MetaData()

# post_table = sqlalchemy.Table(
#     "posts",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("body", sqlalchemy.String),
# )


connect_args = (
    {"check_same_thread": False}
    if config.DATABASE_URL and config.DATABASE_URL.startswith("sqlite")
    else {}
)

sync_database_url = (
    config.DATABASE_URL.replace("postgresql+aiopg://", "postgresql://", 1)
    if config.DATABASE_URL
    else config.DATABASE_URL
)

engine = sqlalchemy.create_engine(
    sync_database_url,
    connect_args=connect_args,
)

metadata.create_all(engine)
database = databases.Database(config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLLBACK)