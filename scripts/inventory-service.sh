#!/bin/bash
declare -r NETWORK="kafka-network"

docker build \
  -f src/inventory_service/Dockerfile \
  -t inventory-service \
  src/inventory_service

docker run -d \
  --name inventory-service \
  --network ${NETWORK} \
  inventory-service
