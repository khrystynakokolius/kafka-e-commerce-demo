import json
from kafka import KafkaConsumer
from variables import VALID_ORDERS_TOPIC, KAFKA_SERVER

consumer = KafkaConsumer(
    VALID_ORDERS_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    group_id='notification-group',
    enable_auto_commit=False,  # Ensures commiting only when processing is successful
    auto_offset_reset='earliest',  # Start at the earliest offset
    fetch_min_bytes=1,  # Get messages as soon as they are available
    fetch_max_wait_ms=50,  # Wait at most 50ms for new data
    max_poll_records=10,  # Small batch size for low-latency
    session_timeout_ms=6000,  # Timeout for detecting dead consumers
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("[Notification Service] Listening to validated orders...", flush=True)

for msg in consumer:
    order = msg.value
    # Assume there is sent an email
    print(f"[Notification Service] Sent order confirmation to customer {order['customer_id']} for order {order['order_id']}", flush=True)
    consumer.commit()