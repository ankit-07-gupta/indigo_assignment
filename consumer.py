# consumer.py
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('flight_notifications', bootstrap_servers='localhost:9092', value_deserializer=lambda m: json.loads(m.decode('utf-8')))

for message in consumer:
    notification = message.value
    print(f"Notification: Flight {notification['flight_id']} status changed to {notification['status']}")
    # Here you can add code to send SMS, email, etc.