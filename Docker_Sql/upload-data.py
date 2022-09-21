#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import pandas as pd
import pyarrow
from sqlalchemy import create_engine
from time import time

def main(params):
    """
    Upload main data
    """
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    data_file = "taxi_data.parquet"
    url = params.url
    
    os.system(f"curl {url} --output {data_file}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    df = pd.read_parquet("taxi_data.parquet",engine='pyarrow')

    df.tpep_pickup_datetime=pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime=pd.to_datetime(df.tpep_dropoff_datetime)

    t_start = time()
    df.to_sql(name=table_name,
                        con=engine,if_exists='replace',
                        chunksize=150000)
    t_end = time()
    print("Insert took %.3f" % (t_end - t_start))

def zone(params):
    """
    Upload zone data
    """
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = "zones"
    data_file = "taxi+_zone_lookup.csv"
    url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"
    
    os.system(f"curl {url} --output {data_file}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    df = pd.read_csv(data_file,engine='pyarrow')

    t_start = time()
    df.to_sql(name=table_name,
                        con=engine,if_exists='replace')
    t_end = time()
    print("Insert took %.3f" % (t_end - t_start))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    # user, password, host, port, database name, url of the csv
    parser.add_argument('--user',help='username for postgres')
    parser.add_argument('--password',help='password for postgres')
    parser.add_argument('--host',help='host name for postgres')
    parser.add_argument('--db',help='db name for postgres')
    parser.add_argument('--port',help='port for postgres')
    parser.add_argument('--table_name',help=' name of the table where we will write the results to')
    parser.add_argument('--url',help='url of the csv file')

    args = parser.parse_args()

    main(args)
    zone(args)
