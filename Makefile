.DEFAULT_GOAL := help
.PHONY: init tests clean
# adjusted for having mkfile_dir to contain abspath to dir in which makefile lies https://stackoverflow.com/a/18137056
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(abspath $(dir $(mkfile_path)))
venv_name := rail-check
app_name := irish_rail_timecheck

create_venv:  ## Creates a virtualenv, called by init
ifneq ($(wildcard $(mkfile_dir)/$(venv_name)),)
	@echo "venv is already exist"
else
	@pip install virtualenv
	@virtualenv ${venv_name}
endif

init: create_venv ## Setup your local env, e.g. create virtual env with dependancies installed.
	@ ./${venv_name}/bin/python -m pip install --requirement requirements.txt
	@ ./${venv_name}/bin/python -m pip install -r requirements-dev.txt

lint: ## Run a lint on app
	./${venv_name}/bin/python -m pylint ${app_name}
	./${venv_name}/bin/python -m flake8 ${app_name} --max-line-length=127
	./${venv_name}/bin/python -m bandit -r ${app_name}

test: init ## Run any tests.
	./${venv_name}/bin/python -m pytest

help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)