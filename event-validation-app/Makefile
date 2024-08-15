SHELL := /bin/bash -o pipefail -o errexit

migrations:
	docker compose exec web python manage.py makemigrations

empty-migration:
	docker compose exec web python manage.py makemigrations --empty $(app_name)

migrate:
	docker compose exec web python manage.py migrate

app:
	docker compose exec web python manage.py startapp $(name)
	sudo chmod -R 0755 $(name)

superuser:
	docker compose exec web python manage.py createsuperuser

collect-static:
	docker compose exec web python manage.py collectstatic

bash:
	docker compose exec web bash

clear-images:
	docker rmi $$(docker images -f 'dangling=true' -q)

on:
	docker compose up

off:
	docker compose down

build:
	docker compose up --build
