import paho.mqtt.client as mqtt
import mysql.connector

# MySQL数据库配置
db_config = {
    'host': 'localhost',
    'user': 'mqttuser',
    'password': 'mqttpassword',  # 替换为你的root密码
    'database': 'mqtt_data'
}

# 连接到数据库
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# MQTT配置
MQTT_BROKER = 'localhost'  # 或其他MQTT服务器地址
MQTT_PORT = 1883
MQTT_TOPIC = 'hdjhdj/newbie'  # 更改为你的MQTT主题


# 当接收到MQTT消息时的回调函数
def on_message(client, userdata, message):
    data = message.payload.decode('utf-8')
    print("Received message:", data)

    # 插入数据到数据库
    try:
        cursor.execute("INSERT INTO mqtt_messages (message_data) VALUES (%s)", (data,))
        conn.commit()
    except Exception as e:
        print("Error saving data to database:", e)


client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT)
client.subscribe(MQTT_TOPIC)
client.on_message = on_message
client.loop_forever()

