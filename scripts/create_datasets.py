from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()
# TODO(developer): Set table_id to the ID of the table to create.
project_id = 'fschwanck-case-gb-2'

# TODO(developer): Set dataset_id to the ID of the dataset to create.
raw_dataset_id = f"{project_id}.raw"
refined_dataset_id = f"{project_id}.refined"

# Construct a full Dataset object to send to the API.
raw_dataset = bigquery.Dataset(raw_dataset_id)
refined_dataset = bigquery.Dataset(refined_dataset_id)



# Send the dataset to the API for creation, with an explicit timeout.
# Raises google.api_core.exceptions.Conflict if the Dataset already
# exists within the project.
dataset = client.create_dataset(raw_dataset, timeout=30, exists_ok=True)  # Make an API request.
dataset = client.create_dataset(refined_dataset, timeout=30, exists_ok=True)  # Make an API request.
print("Created dataset {}.{}".format(client.project, raw_dataset.dataset_id))
print("Created dataset {}.{}".format(client.project, refined_dataset.dataset_id))