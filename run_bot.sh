#!/bin/bash

docker build -t owlbot .
docker run -d -ti --name owlbot --mount type=bind,source=/root/owlbot/authentication/forms,target=/code/authentication/forms owlbot
