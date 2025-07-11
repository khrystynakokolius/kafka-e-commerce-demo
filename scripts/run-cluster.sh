#!/bin/bash

# Define network
declare -r NETWORK="kafka-network"

# Step 1: Create Docker network
if docker network create --driver bridge ${NETWORK}; then
  echo "Successfully created network ${NETWORK}"
else
  echo "Network ${NETWORK} already exists"
fi

# Step 2: Start Docker Compose services
docker-compose -f ./docker/docker-compose.yml up -d

# Step 3: Wait for Kafka to be ready
echo "Waiting for Kafka to start..."
sleep 40

# Step 4: Create Kafka topics
docker run -it --rm --network ${NETWORK} confluentinc/cp-kafka:7.3.0 kafka-topics \
  --create \
  --bootstrap-server kafka:9092 \
  --replication-factor 1 \
  --partitions 3 \
  --topic ecommerce_orders

docker run -it --rm --network ${NETWORK} confluentinc/cp-kafka:7.3.0 kafka-topics \
  --create \
  --bootstrap-server kafka:9092 \
  --replication-factor 1 \
  --partitions 3 \
  --topic valid_orders

docker run -it --rm --network ${NETWORK} confluentinc/cp-kafka:7.3.0 kafka-topics \
  --create \
  --bootstrap-server kafka:9092 \
  --replication-factor 1 \
  --partitions 3 \
  --topic fraud_orders
