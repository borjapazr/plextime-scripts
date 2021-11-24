ROOT_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
SERVICE := plextime-scripts
include $(ROOT_DIR)/common.mk
include .env

.ONESHELL:

.PHONY: install
install: ## Start all containers in background
	@$(DOCKER_COMPOSE) up -d --build

.PHONY: uninstall
uninstall: ## Stop all containers and remove all data
	@$(DOCKER_COMPOSE) down -v
	@sudo rm -rf $(VOLUME_DIR)

.PHONY: journal-options ## List available journal options
journal-options: CMD = journal-options

.PHONY: checkin ## Checkin
checkin: CMD = checkin

.PHONY: checkout ## Checkout
checkout: CMD = checkout

journal-options checkin checkout:
	@[ -n "`$(DOCKER) images -q $(SERVICE)`" ] || $(MAKE) --no-print-directory build
	@$(DOCKER) run --rm --env-file .env $(SERVICE) $(CMD)
