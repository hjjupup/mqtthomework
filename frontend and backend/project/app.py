from flask import Flask, jsonify, render_template
from flask_mqtt import Mqtt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_caching import Cache
from flask_socketio import SocketIO, emit
from datetime import datetime
import json
from random import randint
import os
import subprocess

app = Flask(__name__)

# MQTT Configuration
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_data.db'
db = SQLAlchemy(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)

# Cache Configuration
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
cache = Cache(app)

# SocketIO Initialization
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins for development

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
def handle_connect_socket():
    print('Client connected')
    emit('message', {'data': 'Connected'})

@socketio.on('disconnect')
def handle_disconnect_socket():
    print('Client disconnected')

if __name__ == '__main__':
    # Start Flask app in the background
    subprocess.Popen(["python3", "app.py"])

    # Start Localtunnel to expose the local Flask server
    subprocess.Popen(["lt", "--port", "5001"])



