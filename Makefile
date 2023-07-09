VERSION=latest
SCRIPTS_DIR=./scripts
DOCKER_DIR=./docker
CODE_DIR=source
CERTIFICATES_DIR=./.cache/certificates
LOCAL_CONFIG_DIR=./config/local
BUILD_DIR=./.cache/build
SERVER_DIR=./server
CLIENT_DIR=./client
DOCKER_USER=fschwanck
KUBERNETES_SERVER=blacksabbath.inf.ufrgs.br
SSH_USER=fmschwanck


.PHONY: install-poetry
install-poetry:
	curl -sSL https://install.python-poetry.org | POETRY_HOME=/bin/poetry python3 -
	echo 'export PATH="/bin/poetry/bin:$PATH"' >> ~/.bashrc
	source ~/.bashrc
	poetry config virtualenvs.in-project true


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

