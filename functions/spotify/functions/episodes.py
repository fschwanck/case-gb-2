from functions.function import _SpotifyFunction
from google.cloud import bigquery as bq
import pandas as pd

class SpotifyEpisodes(_SpotifyFunction):
    __jobConfig = bq.LoadJobConfig(
            schema=[
            bq.SchemaField("id", "STRING","NULLABLE",description = "Identificação do episódio"),
            bq.SchemaField("name", "STRING","NULLABLE",description = "Descrição do episódio"),
            bq.SchemaField("description", "STRING","NULLABLE",description = 'Descrição do episódio.'),
            bq.SchemaField("release_date", "DATE","NULLABLE",description = 'Data de lançamento do episódio'),
            bq.SchemaField("duration_ms", "INTEGER","NULLABLE",description = 'Total de episódios lançados até o momento'),
            bq.SchemaField("language", "STRING","NULLABLE",description = 'Idioma do episódio'),
            bq.SchemaField("explicit", "BOOLEAN","NULLABLE",description = 'Flag booleano se o episódio possui conteúdo explícito.'),
            bq.SchemaField("type", "STRING","NULLABLE",description = 'O tipo de faixa de áudio (Ex: música / programa) ')
            ],
            destination_table_description="tabela_6",
            source_format=bq.SourceFormat.NEWLINE_DELIMITED_JSON,
            write_disposition='WRITE_TRUNCATE'
        )

    def __init__(self, projectId: str,datasetId: str,tableId: str):
        super().__init__(projectId,datasetId,tableId)

    def run(self):
       
        data = self._api.getAllShowEpisodes(id='1oMIHOXsrLFENAeM743g93', market='BR')
        df = pd.DataFrame.from_records(data['items'], columns=['id','name','description','release_date', 'duration_ms', 'language', 'explicit', 'type'])
        data = df.to_dict(orient='records')
        self._write_data(data,self.__jobConfig,self._projectId,self._datasetId,self._tableId)


        return 'tabela_6 escrita com sucesso'
