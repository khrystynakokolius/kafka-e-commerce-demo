#!/bin/bash
declare -r NETWORK="kafka-network"

docker build \
  -f src/order_events_producer_service/Dockerfile \
  -t order-events-producer-service \
  src/order_events_producer_service

docker run -d \
  --name order-events-producer-service \
  --network ${NETWORK} \
  order-events-producer-service
