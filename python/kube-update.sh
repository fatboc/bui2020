#!/bin/bash

kubectl delete -f python.yaml
docker build -t fatusia/bui2020:python .
docker push fatusia/bui2020:python
kubectl create -f python.yaml
minikube service list
