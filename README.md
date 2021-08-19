## Egreen (Rambutan version)

Introduction to project, its purposes etc..

## Environment variables for work

* `SECRET_KEY`
* `DOMAIN_NAME`
* `DATABASE_URL`
* `DEBUG` (default: false)

## Develop

### Requirements

* Python
* Docker
* docker-compose
* Make
* Specify env vars in IDE Run Configuration (example in `dev.env`)

Init (is executed once)

```bash
make i
```

Start (doesn't need if was executed the Init)

```bash
make s
```

Getting logs from running containers

```bash
make l
```

Stop containers

```bash
make stop
```

Restart containers

```bash
make r
```

Delete database volume

```bash
make d
```

## Flatpage templates

1. For buyer landing pages use template `buyer/flatpages/default.html`
1. For farmer landing pages use template `farmer/flatpages/default.html`
