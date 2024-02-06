# DineStream

DESCRIPTION

## Installation
```bash
git clone "https://github.com/GrzegorzPustulka/admin_service.git"
cd admin_service
pip install poetry
poetry shell
uvicorn admin_service.main:app
```

## Functionalities
- [x] menu management
- [x] employee management
- [x] category management
- [x] sending emails

### Local server mailhog with docker

```bash
docker run -d -p 1025:1025 -p 8025:8025 --name mailhog mailhog/mailhog
```

```http request
http://localhost:8025
```
