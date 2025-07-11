#!/bin/bash
declare -r NETWORK="kafka-network"

docker build \
  -f src/notification_service/Dockerfile \
  -t notification-service \
  src/notification_service

docker run -d \
  --name notification-service \
  --network ${NETWORK} \
  notification-service
