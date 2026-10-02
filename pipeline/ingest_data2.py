#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine


@click.command()
@click.option("--pg-user", default="root", show_default=True)
@click.option("--pg-pass", default="root", show_default=False)
@click.option("--pg-host", default="localhost", show_default=True)
@click.option("--pg-port", default=5432, type=int, show_default=True)
@click.option("--pg-db", default="ny_taxi", show_default=True)
@click.option("--target-table", default="taxi_zone_lookup", show_default=True)
def load_taxi_zone_lookup(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table):
    url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"

    dtype = {
        "LocationID": "Int64",
        "Borough": "string",
        "Zone": "string",
        "service_zone": "string",
    }

    df = pd.read_csv(url, dtype=dtype)

    engine = create_engine(
        f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    )

    # Create table using the first row as schema and replace if it already exists
    df.head(0).to_sql(name=target_table, con=engine, if_exists="replace", index=False)

    # Insert all rows
    df.to_sql(name=target_table, con=engine, if_exists="append", index=False)

    print(f"Loaded {len(df)} rows into {target_table}")


if __name__ == "__main__":
    load_taxi_zone_lookup()