import os
from sqlalchemy import create_engine, text

DB_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://biuser:bipass@localhost:5432/bi_platform",
)

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(DB_URL)
    return _engine


def load_df(df, table, schema):
    """
    Refresh an existing table while preserving its schema,
    primary keys, and constraints.
    """
    engine = get_engine()

    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {schema}.{table}"))

    df.to_sql(
        table,
        engine,
        schema=schema,
        if_exists="append",
        index=False,
        method="multi",
    )

    print(f"Loaded {len(df)} rows into {schema}.{table}")