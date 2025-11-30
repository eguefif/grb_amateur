#!/bin/sh

docker build -t alertsys .
docker tag alertsys eguefif/grb-amateur:alertsys-latest
docker push eguefif/grb-amateur:alertsys-latest
