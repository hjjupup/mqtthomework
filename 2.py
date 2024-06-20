import paho.mqtt.client as mqtt
import random
import time

HOST = "bemfa.com"
PORT = 9501
client_id = "90895d3545b31d9fed8e574329798f99"

# Connect and subscribe
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe("test")  # Subscribe to topic "test"
        publish_random(client)   # Publish a random number immediately after connecting
    else:
        print(f"Failed to connect, return code {rc}")

# Publish random number periodically
def publish_random(client):
    random_number = random.randint(60, 130)  # Adjust heart rate range to 60 to 130 BPM

    # Generate blood pressure and pulse information
    pulse = random_number * 2  # Simulate pulse (twice the heart rate)
    blood_pressure = random.randint(80, 120)  # Simulate blood pressure range between 80 to 120

    # Print blood pressure and pulse information locally
    print(f"Patient's current heart rate: {random_number} BPM")
    print(f"Patient's current pulse: {pulse}")
    print(f"Patient's current blood pressure: {blood_pressure}")

    # Publish only heart rate information to MQTT server
    client.publish("test", str(random_number))
    print(f"Patient's current heart rate information has been uploaded to MQTT server")

# Message reception
def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic}, Message: {msg.payload.decode()}")

# Subscription success
def on_subscribe(client, userdata, mid, granted_qos):
    print(f"On Subscribed: QoS = {granted_qos}")

# Unexpected disconnection
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Unexpected disconnection. Reconnecting...")

client = mqtt.Client(client_id)
client.username_pw_set("userName", "passwd")
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_disconnect = on_disconnect

try:
    client.connect(HOST, PORT, 60)
except Exception as e:
    print(f"Error connecting to MQTT Broker: {e}")
    exit(1)

client.loop_start()  # Start the non-blocking MQTT main loop

# Publish a random number and print heart rate, pulse, and blood pressure information every second
while True:
    publish_random(client)
    time.sleep(1)  # Execute loop every second