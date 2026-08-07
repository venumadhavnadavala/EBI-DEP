import os

import pandas as pd
from sqlalchemy import create_engine, text

DB_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://biuser:bipass@localhost:5432/bi_platform",
)

_engine = None


def get_engine():
    global _engine

    if _engine is None:
        _engine = create_engine(
            DB_URL,
            pool_pre_ping=True,
        )

    return _engine


def load_df(df, table, schema):
    """
    Refresh an existing table while preserving
    schema, primary keys and constraints.
    """

    engine = get_engine()

    with engine.begin() as conn:

        conn.execute(
            text(f"TRUNCATE TABLE {schema}.{table}")
        )

        df.to_sql(
            table,
            conn,
            schema=schema,
            if_exists="append",
            index=False,
            method="multi",
        )

    print(f"Loaded {len(df)} rows into {schema}.{table}")


def read_df(table, schema):
    engine = get_engine()

    with engine.connect() as conn:
        return pd.read_sql(
            text(f"SELECT * FROM {schema}.{table}"),
            conn,
        )