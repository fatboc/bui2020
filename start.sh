#!/usr/bin/env bash

apply () {
    for i in $@
    do
        if [ $(whoami)=="byq" ] ; then
            docker build -t bui2020:$i $i
            docker push fatusia/bui2020:$i
        fi

        kubectl apply -f $i/$i.yaml
    done
}

kubectl get deployments | grep jaeger || kubectl apply -f https://raw.githubusercontent.com/jaegertracing/jaeger-kubernetes/master/all-in-one/jaeger-all-in-one-template.yml

apply mysql python
