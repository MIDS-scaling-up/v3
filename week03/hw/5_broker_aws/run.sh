#!/bin/bash

#docker network rm hw03
#docker network create --driver bridge hw03

#docker run -it --rm --name broker_nx --network hw03 -p 1883:1883 -v ~/w251/hw03:/hw03 broker_nx mosquitto
docker run -it --rm --name mosquitto --network host -p 1883:1883 -v /tmp:/tmp sudhrity/mosquitto:v2
