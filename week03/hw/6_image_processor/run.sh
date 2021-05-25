#!/bin/bash
docker run --rm -it --name imageprocessor --network host -v ~/data/:/apps/data/ sudhrity/imageprocessor:v1 sh
#docker run --rm -it --name imageprocessor --network host sudhrity/imageprocessor:v1 sh

