from flask_mqtt import Mqtt

mqtt = Mqtt()

def subscribe_to_topic(topic):
    mqtt.subscribe(topic)
