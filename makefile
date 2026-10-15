GITHUB_SA=
PYTHONPATH=.
DOCUMENT_DOCKER_PATH=Documentation/docker-compose.yml

DOCKER_TAG=xxxxxxxxx # https://generate-random.org/hashes md5 128 -> lower


define find.functions
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
endef

help:
	@echo 'The following commands can be used.'
	$(call find.functions)

docs-up: ## Execute docker compose up for docs
	docker compose -f $(DOCUMENT_DOCKER_PATH) up -d 
	docker ps -a

docs-down: ## Drop the container
	docker compose -f $(DOCUMENT_DOCKER_PATH) down 

