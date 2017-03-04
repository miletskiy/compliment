# -*- makefile -*-
SHELL=/bin/bash
# Copyright (с) 2017.

# constants
PROJECT_NAME=Compliment
BIND_TO=0.0.0.0
BIND_TO_WEB=192.168.1.101
BIND_PORT=8042
MANAGE=python manage.py
DJANGO_SETTINGS_MODULE=compliment.settings



include

.PHONY: run open local clean manage help shell ishell  migrate

run:
	@echo Starting $(PROJECT_NAME) with $(DJANGO_SETTINGS_MODULE)...
	$(MANAGE) runserver $(BIND_TO):$(BIND_PORT) --settings=$(DJANGO_SETTINGS_MODULE)

run2:
	@echo Starting $(PROJECT_NAME) local net ...
	$(MANAGE) runserver $(BIND_TO_WEB):$(BIND_PORT) --settings=$(DJANGO_SETTINGS_MODULE)

open:
	@echo Opening $(PROJECT_NAME) ...
	open 'http://$(BIND_TO):$(BIND_PORT)'

clean:
	@echo Cleaning up...
	find ./compliment | grep '\.pyc$$' | xargs -I {} rm {}
	@echo Done

shell:
	# @echo Please, specify this command in the Makefile
	$(MANAGE) shell --plain

ishell:
	$(MANAGE) shell -i ipython

migrate:
ifndef app_name
	$(MANAGE) migrate
else
	@echo Starting of migration of $(app_name)
	$(MANAGE) makemigrations $(app_name)
	$(MANAGE) migrate $(app_name)
	@echo Done
endif

help:
	@cat README.md

# https://github.com/kaleissin/django-makefile/blob/master/Makefile
