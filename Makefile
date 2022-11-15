mmm:
	./manage.py makemigrations --merge

mm:
	./manage.py makemigrations

m:
	./manage.py migrate

cs:
	./manage.py collectstatic --noinput -l

csu:
	./manage.py createsuperuser

du:
	./manage.py create_tree

sh:
	./manage.py shell

i: m cs du

vcs:
	./manage.py versioned_collectstatic
