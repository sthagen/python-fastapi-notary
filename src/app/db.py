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
    Column("topic", String(50)),
    Column("summary", String(150)),
    Column("digest", String(150)),
    Column("source_url", String(150)),
    Column("target_url", String(150)),
    Column("time_ref", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

database = Database(DATABASE_URL)
