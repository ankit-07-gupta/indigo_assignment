# app.py
from flask import Flask, request, jsonify
from pymongo import MongoClient
from kafka import KafkaProducer
import json

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017')
db = client['flight_status']
flights_collection = db['flights']

# Kafka setup
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

@app.route('/flight_status/<flight_id>', methods=['GET'])
def get_flight_status(flight_id):
    flight = flights_collection.find_one({'flight_id': flight_id})
    if flight:
        return jsonify(flight), 200
    else:
        return jsonify({'error': 'Flight not found'}), 404

@app.route('/update_flight_status', methods=['POST'])
def update_flight_status():
    data = request.json
    flight_id = data['flight_id']
    status = data['status']
    flights_collection.update_one({'flight_id': flight_id}, {'$set': {'status': status}}, upsert=True)
    producer.send('flight_notifications', {'flight_id': flight_id, 'status': status})
    return jsonify({'message': 'Flight status updated'}), 200

if __name__ == '__main__':
    app.run(debug=True)