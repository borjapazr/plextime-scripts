## Docker commands ##
DOCKER := docker
DOCKER_COMPOSE := docker-compose
DOCKER_COMPOSE_FILE := $(ROOT_DIR)/docker-compose.yml

## Set 'sh' as default shell ##
SHELL = /bin/sh
## Set 'help' target as the default goal ##
.DEFAULT_GOAL := help

.PHONY: enable
enable: ## Enable service
	@rm -rf .disabled

.PHONY: disable
disable: down ## Disable service
	@touch .disabled

.PHONY: env
env: ## Create .env file from .env.template
	@if [ ! -f .env ]; then cp .env.template .env; fi

.PHONY: health
health: ## Get service health
	@if [ -z `$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) ps -q ${SERVICE}` ] || [ -z `$(DOCKER) ps -q --no-trunc | grep $$($(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) ps -q ${SERVICE})` ]; then echo "DOWN"; else echo "UP"; fi

.PHONY: build
build: CMD = build $(c) ## Build all or c=<name> containers

.PHONY: up
up: CMD = up -d $(c) ## Up all or c=<name> containers

.PHONY: down
down: CMD = down $(c) ## Down all or c=<name> containers

.PHONY: destroy
destroy: CMD = down -v $(c) ## Destroy all or c=<name> containers

.PHONY: start
start: CMD = start $(c) ## Start all or c=<name> containers

.PHONY: stop
stop: CMD = stop $(c) ## Stop all or c=<name> containers

.PHONY: restart
restart: down up ## Restart all or c=<name> containers

.PHONY: status
status: CMD = ps ## Show status of containers

.PHONY: logs
logs: CMD = logs --tail=100 -f $(c) ## Show logs for all or c=<name> containers

build up down start stop destroy logs status:
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) $(CMD)
