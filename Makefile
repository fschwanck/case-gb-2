PROJECT_ID=fschwanck-case-gb-2
BUCKET_NAME=$(PROJECT_ID)-bucket
BUCKET_LOCATION=us


.PHONY: gcp-set-project
gcp-set-project:
	gcloud config set project $(PROJECT_ID)

.PHONY: gcp-create-bucket
gcp-create-bucket:
	gcloud storage buckets create gs://$(BUCKET_NAME) --project=$(PROJECT_ID) --location=$(BUCKET_LOCATION) --uniform-bucket-level-access


.PHONY: gcp-upload-bucket
gcp-upload-bucket: rebuild-base
	gcloud storage cp ./data/base.csv gs://$(BUCKET_NAME)

.PHONY: gcp-init-bucket
gcp-init-bucket: gcp-create-bucket gcp-upload-bucket
	echo "Creating bucket and uploading data to $(BUCKET_NAME}"

.PHONY: gcp-create-datasets
gcp-create-datasets:
	poetry run python3 ./scripts/create_datasets.py

.PHONY: rebuild-base
rebuild-base: 
	poetry run python3 ./scripts/rebuild_base.py

.PHONY: gcp-install-cli:
gcp-install-cli:
	sudo apt-get update
	sudo apt-get install apt-transport-https ca-certificates gnupg curl sudo
	echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
	curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
	sudo apt-get update && sudo apt-get install google-cloud-cli