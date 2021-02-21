"""BigQueryへクエリを発行する"""

from datetime import datetime, timedelta, timezone
from google.cloud import bigquery
import consts
import subprocess

DESTINATION_DATASET = 'test'
DESTINATION_TABLE = 'dest_table'
QUERY_PARAMS_VALUES = {'date': '20210222'}
TIME_PARTITIONIG_TYPE = bigquery.TimePartitioningType.DAY
TIME_PARTITIONIG_COLUMN = 'time_partitioning_column'
CLUSTER_FIELDS = []

# クエリファイルを文字列として展開
with open('./sql/' + DESTINATION_TABLE + '.sql') as f:
    query = f.read()
    print('query:"{}"'.format(query))

client = bigquery.Client(consts.PROJECT_ID)

# クエリ発行時の設定
job_config = bigquery.QueryJobConfig()
job_config.destination = client.dataset(DESTINATION_DATASET).table(DESTINATION_TABLE)
job_config.write_disposition = 'WRITE_TRUNCATE'
job_config.create_disposition = 'CREATE_IF_NEEDED'
job_config.use_legacy_sql = False

# クエリパラメータの設定
if QUERY_PARAMS_VALUES:
    query_params = []
    for key, value in QUERY_PARAMS_VALUES.items():
        print('query parameter name: @{}, value: {}'.format(key, value))
        query_params.append(bigquery.ScalarQueryParameter(key, 'STRING', value))
    job_config.query_parameters = query_params

# パーティションの設定
if TIME_PARTITIONIG_COLUMN:
    print('time_partitioning_cloumn: {}'.format(TIME_PARTITIONIG_COLUMN))
    job_config.time_partitioning = bigquery.TimePartitioning(
        type_=TIME_PARTITIONIG_TYPE,
        field=TIME_PARTITIONIG_COLUMN,
    )
    # クラスタの設定
    if CLUSTER_FIELDS:
        print('cluster_fields: {}'.format(cluster_fields))
        job_config.clustering_fields = cluster_fields

# クエリ発行
query_job = client.query(query, job_config=job_config, location=consts.DEFAULT_LOCATION)
query_job.result()
