# Microservices with Docker, Flask, and React

[![Build Status](https://travis-ci.org/sangtb92/ciand.svg?branch=master)](https://travis-ci.org/sangtb92/ciand)


## Up services
```
//users-db
$ docker-compose -f docker-compose-dev.yml up -d users-db

//kong-migration
$ docker-compose -f docker-compose-dev.yml up -d kong-migration

// all service 
$ docker-compose -f docker-compose-dev.yml up -d

//migrate db
$ docker-compose -f docker-compose-dev.yml run users python manage.py db init
$ docker-compose -f docker-compose-dev.yml run users python manage.py db migrate
$ docker-compose -f docker-compose-dev.yml run users python manage.py db upgrade
```
