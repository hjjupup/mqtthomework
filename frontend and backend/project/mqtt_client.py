from flask_mqtt import Mqtt

mqtt = Mqtt()

def subscribe_to_topic(topic):
    mqtt.subscribe(topic)

# MQTT连接成功时的回调
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # 订阅主题示例
    subscribe_to_topic('topic/test')

# 收到MQTT消息时的回调
@mqtt.on_message()
def handle_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '"
          + message.topic + "' with QoS " + str(message.qos))

if __name__ == '__main__':
    mqtt.client.connect('broker.hivemq.com', 1883, 60)  # 连接到MQTT代理
    mqtt.client.loop_forever()  # 保持连接并处理消息
