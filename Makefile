.PHONY: run db install setup clean showdb
SHELL := /bin/sh
VENV_NAME = env
ENV_DIR := $(CURDIR)/backend/$(VENV_NAME)
BASE_DIR := $(CURDIR)/backend

ifeq ($(OS),Windows_NT)
	PYTHON_PATH := $(ENV_DIR)/Scripts/python
	PIP := $(ENV_DIR)/Scripts/pip
	PYTHON = python

else
	PYTHON_PATH := $(ENV_DIR)/bin/python3
	PIP := $(ENV_DIR)/bin/pip3
	PYTHON = python3
endif

venv:
	$(PYTHON) -m venv ./backend/env

run:
	$(PYTHON_PATH) $(BASE_DIR)/manage.py runserver

db:
	$(PYTHON_PATH) $(BASE_DIR)/manage.py makemigrations
	$(PYTHON_PATH) $(BASE_DIR)/manage.py migrate

install:
	@echo "installing requirements.txt..."
	$(PIP) install -r $(BASE_DIR)/requirements.txt

static:
	$(PYTHON_PATH) $(BASE_DIR)/manage.py collectstatic

setup: venv install db static

showdb:
	$(PYTHON_PATH) $(BASE_DIR)/manage.py showmigrations

clean:
	rm -rf __pycache__
	rm -rf $(BASE_DIR)/$(VENV_NAME)
