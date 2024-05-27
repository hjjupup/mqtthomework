#the base set of database(contant the base operation of mqtt and the creation, initializaion of database )
#一些基本的设置，连接mysql并在database中插入了一些信息，包括了一些mqtt的配置
import paho.mqtt.client as mqtt
import mysql.connector
import sqlite3

# 连接到 MySQL 服务器，蛮多参数要改 connect to sql，some agruments need be charged
mydb = mysql.connector.connect(
    host="localhost",    # 数据库主机地址
    user="root",         # 数据库用户名
    password="jiejiewoaini0",  # 数据库密码，
    database="TheHealthData"    # 数据库名称
)

# 创建一个游标对象
mycursor = mydb.cursor()

# 执行SQL查询
conn = sqlite3.connect('TheHealthData.db')
cursor = conn.cursor()


# 创建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS healthdata_heart_rate (
    username TEXT,
    datetime TEXT,
    heart_rate INT,
    FOREIGN KEY (username) REFERENCES user(username)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS healthdata_blood_pressure (
    username TEXT,
    datetime TEXT,
    systolic INT,
    diastolic INT,
    FOREIGN KEY (username) REFERENCES user(username)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS healthdata_temperature (
    username TEXT,
    datetime TEXT,
    temperature REAL,
    FOREIGN KEY (username) REFERENCES user(username)
);
''')

# 插入一些数据到 SQLite 数据库
cursor.execute("INSERT INTO user (username, password) VALUES ('user1', '123456')")
cursor.execute("INSERT INTO user (username, password) VALUES ('user2', '123456')")

cursor.execute("INSERT INTO healthdata_heart_rate (username, heart_rate) VALUES ('user1', 80)")
cursor.execute("INSERT INTO healthdata_heart_rate (username, heart_rate) VALUES ('user2', 75)")

cursor.execute("INSERT INTO healthdata_blood_pressure (username, systolic, diastolic) VALUES ('user1', 120, 80)")
cursor.execute("INSERT INTO healthdata_blood_pressure (username, systolic, diastolic) VALUES ('user2', 130, 85)")

cursor.execute("INSERT INTO healthdata_temperature (username, temperature) VALUES ('user1', 36.5)")
cursor.execute("INSERT INTO healthdata_temperature (username, temperature) VALUES ('user2', 36.8)")

# 提交事务
conn.commit()

# 关闭 SQLite 连接
conn.close()

# 执行 MySQL 查询
# mycursor.execute("SELECT * FROM healthdata_heart_rate WHERE heart_rate > 50")

# 获取查询结果
result = mycursor.fetchall()

# 打印结果
for row in result:
    print(row)

# MQTT 配置
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC = 'hdjhdj/newbie'

# 当接收到 MQTT 消息时的回调函数
def on_message(client, userdata, message):
    data = message.payload.decode('utf-8')
    print("Received message:", data)

    # 插入数据到数据库
    try:
        mycursor.execute("INSERT INTO mqtt_messages (message_data) VALUES (%s)", (data,))
        mydb.commit()
    except Exception as e:
        print("Error saving data to database:", e)

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT)
client.subscribe(MQTT_TOPIC)
client.on_message = on_message
client.loop_forever()

# 关闭 MySQL 连接
mycursor.close()
mydb.close()