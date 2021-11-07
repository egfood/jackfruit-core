b: docker-compose.yml
	docker-compose build

s: docker-compose.yml
	docker-compose up -d postgres
	sleep 3
	docker-compose up -d web

mmm:
	docker-compose exec web python manage.py makemigrations --merge

mm:
	docker-compose exec web python manage.py makemigrations

m:
	docker-compose exec web python manage.py migrate

cs:
	docker-compose exec web python manage.py collectstatic --noinput -l

csu:
	docker-compose exec web python manage.py createsuperuser

du:
	docker-compose exec web python manage.py create_tree

sh:
	docker-compose exec web python manage.py shell

ba:
	docker-compose exec web bash

i: b s m cs du

l:
	docker-compose logs -f

r:
	docker-compose restart

stop:
	docker-compose stop

d:
	docker-compose down --volumes
	
demo:
	docker-compose exec web python manage.py create_tree

