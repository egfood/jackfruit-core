## Egreen

Introduction to project, its purposes etc..

## Environment variables for work

* `SECRET_KEY`
* `DOMAIN_NAME`
* `DATABASE_URL`
* `DEBUG` (dafault: false)

## Project initialization
#### For build docker, apply migrations and create demo users:
```bash
make i
```

## Develop

* Python
* Docker
* Specify env vars in IDE Run Configuration (example in `dev.env`)

```bash
pip install requirements_prod.txt
docker-compose up -d postgres
./manage.py makemigrations && ./manage.py migrate
./manage.py runserver
```
