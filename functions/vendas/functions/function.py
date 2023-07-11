from google.cloud.bigquery.job.load import LoadJobConfig
from google.cloud import bigquery as bq



class _BucketFunction():
    _bqclient = bq.Client 
    _projectId: str 
    _datasetId: str
    _tableId: str
    _bucket: str
    _file: str
   
    def __init__(self, projectId: str,datasetId: str,tableId: str, _bucket: str, _file: str):
        self._bqclient = bq.Client() 
        self._projectId = projectId
        self._datasetId = datasetId
        self._tableId = tableId
        self._bucket = _bucket
        self._file = _file
        
               
    def _write_data(self, jobConfig: LoadJobConfig, uri: str):
        dataset = bq.DatasetReference(self._projectId, self._datasetId)
        table = dataset.table(self._tableId)
        job = self._bqclient.load_table_from_uri(uri, table, job_config=jobConfig)
        job.result()

        
                
        
    