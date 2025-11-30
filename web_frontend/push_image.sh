#!/bin/sh

docker build -t nginx .
docker tag nginx eguefif/grb-amateur:nginx-latest
docker push eguefif/grb-amateur:nginx-latest
