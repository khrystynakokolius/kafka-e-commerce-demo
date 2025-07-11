from kafka import KafkaConsumer, KafkaProducer
import json
from datetime import datetime
from variables import (
    KAFKA_SERVER,
    ECOMM_ORDERS_TOPIC,
    VALID_ORDERS_TOPIC,
    FRAUD_ORDERS_TOPIC
)

consumer = KafkaConsumer(
    ECOMM_ORDERS_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    group_id='order-processing-group',
    enable_auto_commit=False,      # Ensures commiting only when processing is successful
    auto_offset_reset='earliest',  # Start at the earliest offset
    fetch_min_bytes=1,             # Get messages as soon as they are available
    fetch_max_wait_ms=50,          # Wait at most 50ms for new data
    max_poll_records=10,           # Small batch size for low-latency
    session_timeout_ms=6000,       # Timeout for detecting dead consumers
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def is_suspicious(order):
    """
    Basic fraud rules:
    - very high quantity
    - very high total amount
    - suspicious payment method for such transaction
    """
    total = order['quantity'] * order['price']
    if order['quantity'] > 20:
        return "very high quantity"
    if total > 5000:
        return f"very high order amount ${total}"
    if order['payment_method'] == "bank_transfer" and total > 2000:
        return "suspicious payment method for big transaction"
    return None

def process_order(order):
    """
    Placeholder for order processing logic.
    """
    print(f"Order processed successfully: {order['order_id']} (Customer: {order['customer_id']})")

if __name__ == "__main__":
    print("[Order Router] Listening for orders...")

    for message in consumer:
        order = message.value
        print(f"Received order: {order['order_id']}")

        # Check for fraud
        reason = is_suspicious(order)
        if reason:
            order['fraudulent'] = True
            fraud_alert = {
                "alert_id": order['event_id'],
                "order_id": order['order_id'],
                "reason": reason,
                "order_details": order,
                "timestamp": datetime.utcnow().isoformat()
            }
            producer.send(FRAUD_ORDERS_TOPIC, value=fraud_alert)
            print(f"Fraud detected: {reason} - routed to {FRAUD_ORDERS_TOPIC} and alert sent")
        else:
            order['validated_at'] = datetime.utcnow().isoformat()
            producer.send(VALID_ORDERS_TOPIC, value=order)
            process_order(order)
            print(f"Valid order routed to {VALID_ORDERS_TOPIC}")
        consumer.commit()
