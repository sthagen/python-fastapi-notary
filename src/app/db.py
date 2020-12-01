import os

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        create_engine)
from sqlalchemy.sql import func

from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
metadata = MetaData()
notes = Table(
    "notary",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("tag", String(50)),
    Column("summary", String(50)),
    Column("hash", String(50)),
    Column("local_time", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

database = Database(DATABASE_URL)
