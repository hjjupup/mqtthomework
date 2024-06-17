from flask import Flask, jsonify, render_template
from flask_mqtt import Mqtt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_caching import Cache
from datetime import datetime
import json
from random import randint

appN = Flask(__name__)

# MQTT Configuration
appN.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
appN.config['MQTT_BROKER_PORT'] = 1883
appN.config['MQTT_USERNAME'] = ''
appN.config['MQTT_PASSWORD'] = ''
appN.config['MQTT_KEEPALIVE'] = 60
appN.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(appN)

# Database Configuration
appN.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_data.db'
db = SQLAlchemy(appN)

# JWT Configuration
appN.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(appN)

# Cache Configuration
appN.config['CACHE_TYPE'] = 'RedisCache'
appN.config['CACHE_REDIS_HOST'] = 'localhost'
appN.config['CACHE_REDIS_PORT'] = 6379
appN.config['CACHE_REDIS_DB'] = 0
appN.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
cache = Cache(appN)

class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    topic = db.Column(db.String(50), nullable=False)
    payload = db.Column(db.String(200), nullable=False)

def generate_random_data():
    heartbeat = randint(60, 120)  # 60-120之间的随机数
    pulse = randint(60, 120)      # 60-120之间的随机数
    blood_pressure = f"{randint(110, 130)}/{randint(70, 90)}"  # 随机生成血压值
    return {
        'heartbeat': heartbeat,
        'pulse': pulse,
        'blood_pressure': blood_pressure
    }

def init_data():
    for _ in range(50):  # 初始化50条数据
        data = generate_random_data()
        health_data = HealthData(
            topic='health/monitor',
            payload=json.dumps(data)
        )
        db.session.add(health_data)
    db.session.commit()

@appN.route('/')
def index():
    return render_template('index.html')

@appN.route('/data')
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

if __name__ == '__main__':
    with appN.app_context():
        db.create_all()
        # Initialize the database with test data if needed
        init_data()
    appN.run(debug=True, port=5001)

