from functions.function import _SpotifyFunction
from google.cloud import bigquery as bq
import pandas as pd

class SpotifySearch(_SpotifyFunction):
    __jobConfig = bq.LoadJobConfig(
            schema=[
            bq.SchemaField("id", "STRING","NULLABLE",description = "Identificador único do programa"),
            bq.SchemaField("name", "STRING","NULLABLE",description = "Nome do poscast"),
            bq.SchemaField("description", "STRING","NULLABLE",description = 'Descrição sobre o programa de poscast'),
            bq.SchemaField("total_episodes", "INTEGER","NULLABLE",description = 'Total de episódios lançados até o momento')
            ],
            destination_table_description="tabela_5",
            source_format=bq.SourceFormat.NEWLINE_DELIMITED_JSON,
            write_disposition='WRITE_TRUNCATE'
        )


    def __init__(self, projectId: str,datasetId: str,tableId: str):
        super().__init__(projectId,datasetId,tableId)

    def run(self):
        
        
        data = self._api.getSearch('data hackers','show', market='BR', limit=50, offset=0)
        df = pd.DataFrame.from_records(data['shows']['items'], columns=['id','name','description','total_episodes'])
        data = df.to_dict(orient='records')
        self._write_data(data,self.__jobConfig,self._projectId,self._datasetId,self._tableId)


        return 'tabela_5 escrita com sucesso'
