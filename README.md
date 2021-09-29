# kuptelefonik

## Short description

Django app which helps people buying a new phone buy it in the lowest price. 
It allows to add couple phones to observed view, and then you can analyze price in time and compare offers from different online shops. 
You get e-mail notifications when price has changed.

I am realising this project as the final thesis in University of Lodz, Data Analysis degree.

## MVP Screencast

As a MVP I want to deliver something like this:

https://user-images.githubusercontent.com/53168617/115224315-01b1ac00-a10d-11eb-9aa7-011a9a5339b0.mov


## Development

You need to have Docker installed in your system.

If you want to develop new features and run project locally, you need to:
1. Clone repo
```
git clone git@github.com:damianwasik98/kuptelefonik.git
```
2. Run code
```
cd src && docker-compose up -d
```
3. Load admin theme dump
```
docker-compose exec kuptelefonik python manage.py loaddata admin_interface_theme_kuptelefonik
```
5. Collect static files and run migrations
```
docker-compose exec kuptelefonik python manage.py migrate
docker-compose exec kuptelefonik python manage.py collectstatic
```

### Services URLs
All services ports and other variables are defined in `docker-compose.yaml` file.

`django app`: http://localhost:8000

`django admin`: http://localhost:8000/admin

`celery flower`: http://localhost:5555

`rabbitmq management`: http://localhost:15672
