import os

from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://biuser:bipass@localhost:5432/bi_platform",
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


def query(sql: str, params: dict | None = None):
    """
    Execute a SQL query and return rows as a list of dictionaries.
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        return [dict(row._mapping) for row in result]