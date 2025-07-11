import json
import random
import time
from datetime import datetime
from faker import Faker
from kafka import KafkaProducer
from variables import ECOMM_ORDERS_TOPIC, KAFKA_SERVER

fake = Faker()

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    key_serializer=str.encode, # Serialize the message key into bytes
    value_serializer=lambda v: json.dumps(v).encode('utf-8'), # Serialize the message value: convert Python dict -> JSON string -> UTF-8 bytes
    acks='all', # Wait for acknowledgments from all in-sync replicas
    retries=5, # Retry up to 5 times if a send fails
    compression_type='gzip' # Compress messages using gzip to reduce network traffic and improve throughput
)

customers = [fake.uuid4() for _ in range(10)]
products = [fake.uuid4() for _ in range(10)]

def generate_order_event():
    return {
        "event_id": fake.uuid4(),
        "order_id": fake.uuid4(),
        "customer_id": random.choice(customers),
        "product_id": random.choice(products),
        "quantity": random.randint(1, 100),
        "price": round(random.uniform(10, 5000), 2),
        "timestamp": datetime.utcnow().isoformat(),
        "status": "created",
        "payment_method": random.choice(["credit_card", "paypal", "bank_transfer"]),
        "shipping_address": fake.address()
    }

if __name__ == "__main__":
    while True:
        order_event = generate_order_event()
        future = producer.send(ECOMM_ORDERS_TOPIC, key=order_event['customer_id'], value=order_event)
        try:
            future.get(timeout=10)
            print(f"Produced order event: {order_event}")
        except Exception as e:
            print(f"Failed to deliver message: {e}")
        time.sleep(random.uniform(0.1, 0.5))
