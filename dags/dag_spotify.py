

# ===========================================================================================
# BIBLIOTECAS
# ===========================================================================================

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime, timedelta
from airflow.models import Variable
from airflow import utils



# ===========================================================================================
# VARIÁVEIS
# ===========================================================================================

# Coleta variaveis do Airflow
env_var = Variable.get("dag_spotify", deserialize_json=True)
# Variaveis de Projeto
SCHEDULE_INTERVAL = env_var["schedule_interval"]
RETRIES = env_var["retries"]
RETRY_DELAY = env_var["retry_delay"]
DAG_TIMEOUT = env_var["dag_timeout"]
PROJECT_ID = env_var["project_id"]
DATASET_ID = env_var["dataset_id"]
GCF_URL = env_var["gcf_url"]



# Step 1: Default Arguments - Define default and DAG-specific arguments
default_args = {
    'owner': 'felipe',
    'start_date': utils.dates.days_ago(0),
    'retries': RETRIES,
    'retry_delay': timedelta(minutes=RETRY_DELAY),
    'dagrun_timeout': timedelta(minutes=DAG_TIMEOUT)
}



# Step 2: Instantiate a DAG - Give the DAG name, configure the schedule, and set the DAG settings
dag = DAG(
    'dag_spotify',
    default_args=default_args,
    description='DAG para carga de dados Spotify',
    catchup=False,
    schedule_interval=SCHEDULE_INTERVAL
)
with dag:
    task_load_spotify_search = BashOperator(
        task_id="task_load_spotify_search",
        bash_command=f'curl -X POST "{GCF_URL}?endpoint=search&tableId=tabela_5&projectId={PROJECT_ID}&datasetId={DATASET_ID}" -H "Authorization: bearer $(gcloud auth print-identity-token)"'
    )

    task_load_spotify_episodes = BashOperator(
        task_id="task_load_spotify_episodes",
        bash_command=f'curl -X POST "{GCF_URL}?endpoint=episodes&tableId=tabela_6&projectId={PROJECT_ID}&datasetId={DATASET_ID}" -H "Authorization: bearer $(gcloud auth print-identity-token)"'
    )

    call_stored_procedure_tabela_7 = BigQueryInsertJobOperator(
    task_id="call_stored_procedure_tabela_7",
    configuration={
        "query": {
            "query": f"CALL `{PROJECT_ID}.refined.tabela_7`(); ",
            "useLegacySql": False,
        }
    },
    location='us'
    )
  
  
    [task_load_spotify_search, task_load_spotify_episodes]
    task_load_spotify_episodes >> call_stored_procedure_tabela_7



    




