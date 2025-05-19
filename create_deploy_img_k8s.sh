#!/bin/sh
set -x

echo "Building Docker image: $1"
docker build -t "$1" . || exit 1

echo "Loading image into Minikube: $1"
minikube image load "$1" || exit 1

echo "Applying Kubernetes manifests: $2"
kubectl apply -f "$2" || exit 1
