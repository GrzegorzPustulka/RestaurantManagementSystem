# DineStream

Service for managing a restaurant. It allows you to manage the menu, employees, and categories.

## links to the app

<b>Admin Service:</b>
- [swagger](https://adminservice-production.up.railway.app/docs)
- [redoc](https://adminservice-production.up.railway.app/redoc)

<b>Customer Service</b>
- future link

<b>Kitchen Service</b>
- future link

<b>Restaurant Service</b>
- future link

<b>E-mail Sender Service</b>
- future link


## Installation
```bash
git clone "https://github.com/GrzegorzPustulka/admin_service.git"
cd admin_service
pip install poetry
poetry shell
hypercorn admin_service.main:app --reload
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

```http
http://localhost:8025
```

### Local RabbitMQ with docker

```bash
docker run -d --rm --name rabbitmq -p 5552:5552 -p 5672:5672 -p 15672:15672 -e RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS='-rabbitmq_stream advertised_host localhost' rabbitmq:3.12-management
```
 - login: guest
 - password: guest

```http
http://localhost:15672
```
