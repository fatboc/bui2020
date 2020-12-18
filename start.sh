#!/bin/bash

kubectl delete -f jaeger/jaeger.yaml
kubectl delete -f mysql/mysql-pv.yaml
kubectl delete -f mysql/mysql.yaml
kubectl delete -f python/python.yaml

kubectl create -f jaeger/jaeger.yaml
kubectl create -f mysql/mysql-pv.yaml
kubectl create -f mysql/mysql.yaml
kubectl create -f python/python.yaml
