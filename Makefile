build_dev:
	docker-compose build
up:
	docker-compose up -d
	docker-compose logs -f
migrate:
	docker-compose run --rm web python manage.py migrate
makemi:
	docker-compose  run --rm web python manage.py makemigrations
colstat:
	docker-compose run --rm web python manage.py collectstatic --noinput -l
i:
	docker-compose build && sleep 30 && docker-compose run --rm web python manage.py migrate && docker-compose run --rm web python manage.py demo_users create


