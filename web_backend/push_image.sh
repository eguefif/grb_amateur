#!/bin/sh

docker build -t backend .
docker tag backend eguefif/grb-amateur:backend-latest
docker push eguefif/grb-amateur:backend-latest
