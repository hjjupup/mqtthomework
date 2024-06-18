from flask import Flask, jsonify, render_template
from flask_mqtt import Mqtt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_socketio import SocketIO, emit
from datetime import datetime
import json
from random import randint
import os
import subprocess
import time

app = Flask(__name__)

# MQTT配置
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_data.db'
db = SQLAlchemy(app)

# JWT配置
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)

# 缓存配置
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
cache = Cache(app)

# SocketIO初始化
socketio = SocketIO(app, cors_allowed_origins="*")  # 允许所有来源进行跨域请求（开发环境）

class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    topic = db.Column(db.String(50), nullable=False)
    payload = db.Column(db.String(200), nullable=False)

def generate_random_data():
    heartbeat = randint(60, 120)
    pulse = randint(60, 120)
    blood_pressure = f"{randint(110, 130)}/{randint(70, 90)}"
    return {
        'heartbeat': heartbeat,
        'pulse': pulse,
        'blood_pressure': blood_pressure
    }

def init_data():
    for _ in range(50):
        data = generate_random_data()
        health_data = HealthData(
            topic='health/monitor',
            payload=json.dumps(data)
        )
        db.session.add(health_data)
    db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
@cache.cached(timeout=60)
def get_data():
    data = HealthData.query.order_by(HealthData.timestamp.desc()).all()
    return jsonify([{
        'timestamp': data_item.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'topic': data_item.topic,
        'payload': data_item.payload
    } for data_item in data])

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('health/#')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = HealthData(topic=message.topic, payload=message.payload.decode())
    db.session.add(data)
    db.session.commit()

@socketio.on('connect')
def handle_connect():
    print('客户端已连接')
    emit('message', {'data': '已连接'})

@socketio.on('disconnect')
def handle_disconnect():
    print('客户端已断开连接')

if __name__ == '__main__':
    # 使用localtunnel来公开你的本地Flask应用
    # 在后台启动Flask应用
    flask_process = subprocess.Popen(['python3', 'app.py'])

    # 等待Flask应用启动（根据需要调整等待时间）
    time.sleep(5)

    # 使用localtunnel将端口5001公开到一个公共URL
    localtunnel_process = subprocess.Popen(['lt', '--port', '5001'])

    # 可选：打印localtunnel URL
    print(" * Localtunnel URL: https://your_subdomain.loca.lt")

    try:
        # 等待两个进程结束
        flask_process.wait()
        localtunnel_process.wait()
    except KeyboardInterrupt:
        # 处理键盘中断
        flask_process.terminate()
        localtunnel_process.terminate()
        print(" * 进程已终止.")




