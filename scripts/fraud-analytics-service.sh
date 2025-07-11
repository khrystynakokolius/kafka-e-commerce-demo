#!/bin/bash
declare -r NETWORK="kafka-network"

docker build \
  -f src/fraud_analytics_service/Dockerfile \
  -t fraud-analytics-service \
  src/fraud_analytics_service

docker run -d \
  --name fraud-analytics-service \
  --network ${NETWORK} \
  fraud-analytics-service
