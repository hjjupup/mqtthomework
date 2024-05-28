import paho.mqtt.client as mqtt
import sqlite3
import json
from datetime import datetime

# 数据库连接
conn = sqlite3.connect('TheHealthData.db')
cursor = conn.cursor()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("healthdata/#")  # 订阅所有与健康数据相关的主题

def on_message(client, userdata, msg):
    print(f"Message received on {msg.topic} with data {msg.payload}")
    data = json.loads(msg.payload)

    # 插入数据到对应的表
    if 'heart_rate' in msg.topic:
        cursor.execute("INSERT INTO healthdata_heart_rate (username, datetime, heart_rate) VALUES (?, ?, ?)",
                       (data['username'], data['datetime'], data['heart_rate']))
    elif 'blood_pressure' in msg.topic:
        cursor.execute("INSERT INTO healthdata_blood_pressure (username, datetime, systolic, diastolic) VALUES (?, ?, ?, ?)",
                       (data['username'], data['datetime'], data['systolic'], data['diastolic']))
    elif 'temperature' in msg.topic:
        cursor.execute("INSERT INTO healthdata_temperature (username, datetime, temperature) VALUES (?, ?, ?)",
                       (data['username'], data['datetime'], data['temperature']))
    conn.commit()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt_broker_address", 1883, 60)  # 替换为你的MQTT broker地址和端口
client.loop_forever()  # 持续监听消息
