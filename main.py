from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
project_id = 'fschwanck-case-gb-2'
dataset_id = 'raw'
table_id = f"{project_id}.{dataset_id}.tabela_base"

job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("ID_MARCA", "INTEGER"),
        bigquery.SchemaField("MARCA", "STRING"),
        bigquery.SchemaField("ID_LINHA", "INTEGER"),
        bigquery.SchemaField("LINHA", "STRING"),
        bigquery.SchemaField("DATA_VENDA", "DATE"),
        bigquery.SchemaField("QTD_VENDA", "INTEGER"),
    ],
    skip_leading_rows=1,
    source_format=bigquery.SourceFormat.CSV,
    write_disposition='WRITE_TRUNCATE'
)
uri = "gs://fschwanck-case-gb-2-bucket/base.csv"

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.

load_job.result()  # Wait for the job to complete.

table = client.get_table(table_id)
print("Loaded {} rows to table {}".format(table.num_rows, table_id))