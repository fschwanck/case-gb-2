from functions.function import _BucketFunction
from google.cloud import bigquery as bq

class BaseTable(_BucketFunction):
    __job_config = bq.LoadJobConfig(
            schema=[
                bq.SchemaField("ID_MARCA", "INTEGER"),
                bq.SchemaField("MARCA", "STRING"),
                bq.SchemaField("ID_LINHA", "INTEGER"),
                bq.SchemaField("LINHA", "STRING"),
                bq.SchemaField("DATA_VENDA", "DATE"),
                bq.SchemaField("QTD_VENDA", "INTEGER"),
            ],
            skip_leading_rows=1,
            source_format=bq.SourceFormat.CSV,
            write_disposition='WRITE_TRUNCATE'
            )


    def __init__(self,  projectId: str,datasetId: str,tableId: str,bucket: str, file: str):
        super().__init__( projectId,datasetId,tableId, bucket,file)

    def run(self):
        
        uri = f"gs://{self._bucket}/{self._file}.csv"
        self._write_data(self.__job_config, uri)

        return 'tabela_base escrita com sucesso'


