#!/bin/bash
declare -r NETWORK="kafka-network"

docker build \
  -f src/order_service/Dockerfile \
  -t consume-orders-service \
  src/order_service

docker run -d \
  --name consume-orders-service \
  --network ${NETWORK} \
  consume-orders-service
