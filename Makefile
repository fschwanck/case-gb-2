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

docker-build-client: ${DOCKER_DIR}/client/Dockerfile certificates
	poetry export -C $(CLIENT_DIR) --without-hashes --format=requirements.txt > ${DOCKER_DIR}/client/requirements.txt
	docker build -t '$(DOCKER_USER)/fl-framework-client:${VERSION}'  -f ${DOCKER_DIR}/client/Dockerfile .
	docker push $(DOCKER_USER)/fl-framework-client:${VERSION}

docker-build-server: ${DOCKER_DIR}/server/Dockerfile certificates
	poetry export -C $(SERVER_DIR) --without-hashes --format=requirements.txt > ${DOCKER_DIR}/server/requirements.txt
	docker build -t '$(DOCKER_USER)/fl-framework-server:${VERSION}'  -f ${DOCKER_DIR}/server/Dockerfile .
	docker push $(DOCKER_USER)/fl-framework-server:${VERSION}

.PHONY: local-run-client
local-run-client: 
	poetry run -C $(CLIENT_DIR) sh ${CLIENT_DIR}/run.sh ${CONFIG_FILE}

.PHONY: local-run-server
local-run-server: 
	poetry run -C $(SERVER_DIR) sh ${SERVER_DIR}/run.sh ${CONFIG_FILE}

