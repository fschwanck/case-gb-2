from google.cloud.bigquery.job.load import LoadJobConfig
from functions.api import SpotifyAPI
from google.cloud import bigquery as bq
import os



class _SpotifyFunction():
    _api: SpotifyAPI
    _bqclient = bq.Client 
    _projectId: str 
    _datasetId: str
    _tableId: str
   
    def __init__(self, projectId: str,datasetId: str,tableId: str):
        clientId = os.getenv('clientId')
        clientSecret = os.getenv('clientSecret')
        self._api = SpotifyAPI()
        self._api.auth(clientId=clientId, clientSecret=clientSecret)
        self._bqclient = bq.Client() 
        self._projectId = projectId
        self._datasetId = datasetId
        self._tableId = tableId
        
               
    def _write_data(self, data: dict, jobConfig: LoadJobConfig, projectName: str, datasetName: str, tableName: str):
        dataset = bq.DatasetReference(self._projectId, self._datasetId)
        table = dataset.table(self._tableId)
        
        # Insert JSONL file into Big Query
        job = self._bqclient.load_table_from_json(data,table,job_config=jobConfig)
        job.result()

