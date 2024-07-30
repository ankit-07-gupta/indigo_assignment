# mock_data.py
import requests
import time

flight_updates = [
    {'flight_id': 'ABC123', 'status': 'On Time'},
    {'flight_id': 'ABC123', 'status': 'Delayed'},
    {'flight_id': 'ABC123', 'status': 'Cancelled'},
]

for update in flight_updates:
    requests.post('http://localhost:5000/update_flight_status', json=update)
    time.sleep(10) 