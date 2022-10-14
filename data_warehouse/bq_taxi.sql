CREATE OR REPLACE EXTERNAL TABLE `dynamic-shift-363106.nytaxi.fhv_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dtc_data_lake_dynamic-shift-363106/raw/fhv_tripdata/2019/fhv_tripdata_*.parquet']
);

