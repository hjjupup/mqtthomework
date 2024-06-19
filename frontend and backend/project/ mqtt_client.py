import paho.mqtt.client as mqtt
import json
import time
from random import randint

# MQTT Broker
broker_url = 'broker.hivemq.com'
broker_port = 1883

# Function to generate random health data
def generate_random_data():
    heartbeat = randint(60, 120)
    pulse = randint(60, 120)
    blood_pressure = f"{randint(110, 130)}/{randint(70, 90)}"
    return {
        'heartbeat': heartbeat,
        'pulse': pulse,
        'blood_pressure': blood_pressure
    }

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe('health/monitor')

def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_url, broker_port, 60)

while True:
    data = generate_random_data()
    payload = json.dumps(data)
    client.publish('health/monitor', payload)
    print(f"Published message: {payload}")
    time.sleep(5)
