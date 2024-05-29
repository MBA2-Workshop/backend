# Django Boilerplate

## Docker

### Environment

Create **.env** file with the following content, you can find this in the **.env.sample** file. Replace the values with your own.

```
DEBUG=True #True or False
ALLOWED_HOSTS=127.0.0.1,localhost #split by ","
BASE_URL=http://localhost:8000/
CORS_ALLOWED_ORIGINS=http://127.0.0.1,http://localhost #split by ","
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@admin.com
DJANGO_SUPERUSER_PASSWORD=password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=admin@admin.com
EMAIL_HOST_PASSWORD=password
```

### Build

`docker-compose build `

### Run

`docker-compose up`

## Endpoints

### Server

[http://localhost:8000](http://localhost:8000)

**Admin panel** :
[http://localhost:8000/admin](http://localhost:8000/admin)

- Username: ${DJANGO_SUPERUSER_USERNAME}
- Password: ${DJANGO_SUPERUSER_PASSWORD}

### PgAdmin (database access)

[http://localhost:5050](http://localhost:5050)

In PgAdmin panel you need to add a new server (_Add New Server_):

- General > Name: ${POSTGRES_DB}
- Connection > Host name/address: db
- Connection > Username: ${POSTGRES_USER}
- Connection > Password: ${POSTGRES_PASSWORD}

Next, you need to save the server and then you can access the database.
