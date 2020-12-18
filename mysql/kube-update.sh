#!/bin/bash

kubectl delete -f mysql.yaml
docker build -t fatusia/bui2020:mysql .
docker push fatusia/bui2020:mysql
kubectl create -f mysql.yaml
minikube service list
