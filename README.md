## Egreen (Jackfruit version)

Introduction to project, its purposes etc..

## Environment variables for work

* `SECRET_KEY`
* `DOMAIN_NAME`
* `DATABASE_URL`
* `DEBUG` (default: false)

## Develop

### Requirements

* Python 3.10 (see issue with 3.11 follow the link https://github.com/egfood/jackfruit-core/issues/68)
* Make
* Specify env vars in IDE Run Configuration (example in `dev.env`)

### How to prepare for development (without docker)

1. go to project folder (in jackfruit-core folder)
2. `cp dev.env core/.env`
3. `python3 -m venv py310` (py310 - folder for a new virtual environment)
4. `source py310/bin/activate`
5. `pip install -r requirements.txt`
6. `make i` - applies migrations, collects static and creates demo users (see email/password in output)
7. `make csu` - creates a superuser

After that you can start your server by PyCharm or your preferred IDE or via execute command `./manage.py runserver`'

## Flatpage templates

1. For buyer landing pages use template `buyer/flatpages/default.html`
1. For farmer landing pages use template `farmer/flatpages/default.html`
