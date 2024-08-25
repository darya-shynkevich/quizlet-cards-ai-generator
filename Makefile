.EXPORT_ALL_VARIABLES:
DOTENV_BASE_FILE ?= .env-local
DOTENV_CUSTOM_FILE ?= .env-custom

POETRY_EXPORT_OUTPUT = requirements.txt
POETRY_EXTRAS =
POETRY_GROUPS = --with dev,test
POETRY_PUBLISH_PRERELEASE ?= false
POETRY_VERSION = 1.8.3
POETRY_VIRTUALENVS_CREATE ?= true
POETRY ?= $(HOME)/.local/bin/poetry

PYTHON_INSTALL_PACKAGES_USING ?= poetry
PYTHON_VERSION ?= 3.11.8
PYTHONPATH := $(PYTHONPATH):$(CURDIR)/proto/

-include $(DOTENV_BASE_FILE)
-include $(DOTENV_CUSTOM_FILE)


.PHONY: install-poetry
install-poetry:
ifeq ($(POETRY_PREINSTALLED), true)
	$(POETRY) self update $(POETRY_VERSION)
else
	curl -sSL https://install.python-poetry.org | python -
endif

.PHONY: configure-poetry
configure-poetry:
	@$(POETRY) config repositories.artifactory $(ARTIFACTORY_PYPI_REPOSITORY)
	@$(POETRY) config http-basic.artifactory $(ARTIFACTORY_USERNAME) $(ARTIFACTORY_PASSWORD)
ifeq ($(POETRY_VIRTUALENVS_CREATE), true)
	$(POETRY) env use $(PYTHON_VERSION)
endif

.PHONY: install-packages
install-packages:
ifeq ($(PYTHON_INSTALL_PACKAGES_USING), poetry)
	$(POETRY) install -vv $(POETRY_EXTRAS) $(POETRY_GROUPS) $(opts)
else
	$(POETRY) run pip install \
		--no-index \
		--requirement=$(POETRY_EXPORT_OUTPUT)
endif

.PHONY: install
install: install-poetry configure-poetry install-packages

.PHONY: update-packages
update-packages:
	$(POETRY) update -vvv

.PHONY: lint-bandit
lint-bandit:
	$(POETRY) run bandit --ini .bandit --recursive

.PHONY: lint-black
lint-black:
	$(POETRY) run black --check --diff .

.PHONY: lint-flake8
lint-flake8:
	$(POETRY) run flake8

.PHONY: lint-isort
lint-isort:
	$(POETRY) run isort --check-only --diff .

.PHONY: lint-mypy
lint-mypy:
	$(POETRY) run mypy

.PHONY: lint
lint: lint-bandit lint-black lint-flake8 lint-isort lint-mypy

.PHONY: fmt
fmt:
	- $(POETRY) run isort .
	$(POETRY) run black .

.PHONY: test
test:
	$(POETRY) run pytest $(opts) $(call tests,.)