#!/bin/bash

find mysql-docker -name "*.yaml" -exec kubectl create -f {}\;
find php-docker -name "*.yaml" -exec kubectl create -f {}\;
#find traefik-docker -name "*.yaml" -exec kubectl create -f {}\;
