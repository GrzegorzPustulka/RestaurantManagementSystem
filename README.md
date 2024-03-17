# DineStream

Service for managing a restaurant. It allows you to manage the menu, employees, and categories.

## links to the app

<b>Admin Service:</b>
- [repository](https://github.com/GrzegorzPustulka/admin_service.git)
- [swagger](https://localhost:8000/docs)
- [redoc](https://localhost:8000/redoc)

<b>Customer Service</b>
- [repository](https://github.com/GrzegorzPustulka/customder_service.git)

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
uvicorn admin_service.main:app --reload
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

### Local PostgreSQL with docker

```bash
docker run --name DineStream-postgres -e POSTGRES_PASSWORD=secretPassword -p 5432:5432 -d postgres
```
