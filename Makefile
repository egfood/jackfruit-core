b: docker-compose.yml
	docker-compose build

s: docker-compose.yml
	docker-compose up -d postgres
	sleep 3
	docker-compose up -d web

mm:
	docker-compose exec web python manage.py makemigrations

m:
	docker-compose exec web python manage.py migrate

cs:
	docker-compose exec web python manage.py collectstatic --noinput -l

du:
	docker-compose exec web python manage.py demo_users create

sh:
	docker-compose exec web python manage.py shell

i: s m cs du

l:
	docker-compose logs -f

r:
	docker-compose restart

stop:
	docker-compose stop

d:
	docker-compose down --volumes
