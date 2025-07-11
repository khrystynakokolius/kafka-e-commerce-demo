import json
from kafka import KafkaConsumer
from variables import FRAUD_ORDERS_TOPIC, KAFKA_SERVER

consumer = KafkaConsumer(
    FRAUD_ORDERS_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    group_id='fraud-analytics',
    enable_auto_commit=False,  # Ensures commiting only when processing is successful
    auto_offset_reset='earliest',  # Start at the earliest offset
    fetch_min_bytes=1,  # Get messages as soon as they are available
    fetch_max_wait_ms=50,  # Wait at most 50ms for new data
    max_poll_records=10,  # Small batch size for low-latency
    session_timeout_ms=6000,  # Timeout for detecting dead consumers
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("[Fraud Analytics] Listening for fraud orders...")

for msg in consumer:
    fraud_alert = msg.value
    # Assume there is sent an alert on fraud
    print(f"[Fraud Analytics] Fraud detected: Order {fraud_alert['order_id']}, order details: {fraud_alert['order_details']}, reason: {fraud_alert['reason']}, timestamp:  {fraud_alert['timestamp']}")
    consumer.commit()

