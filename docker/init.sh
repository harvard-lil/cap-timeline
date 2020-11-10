#!/bin/bash

docker-compose up -d

sleep 5

docker-compose exec db createdb research --user postgres

docker-compose exec web python ./manage.py migrate
