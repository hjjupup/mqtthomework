#generate data in 7 days randomly
import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect('TheHealthData.db')

# 执行 SQL 语句对象，这个叫游标
cursor = conn.cursor()

# table creation创建表
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

# 添加示例数据，同时插入时间信息
cursor.execute("INSERT INTO user (username, password) VALUES ('user1', '123456')")
cursor.execute("INSERT INTO user (username, password) VALUES ('user2', '123456')")

# 随机添加10组数据，在一周之内的
start_date = datetime.strptime('2024-05-24 08:00:00', '%Y-%m-%d %H:%M:%S')
for _ in range(10):
    username = random.choice(['user1', 'user2'])
    random_minutes = random.randint(0, 10080)  # 一周的，7天数据
    measured_datetime = start_date + timedelta(minutes=random_minutes)

    # 随机生成数据，插入的是相对健康的数据
    heart_rate = random.randint(60, 100)
    systolic = random.randint(110, 140)
    diastolic = random.randint(70, 90)
    temperature = round(random.uniform(36.0, 37.5), 1)

    # sql插入
    cursor.execute(
        "INSERT INTO healthdata_heart_rate (username, datetime, heart_rate) VALUES (?, ?, ?)",
        (username, measured_datetime.strftime('%Y-%m-%d %H:%M:%S'), heart_rate)
    )

    cursor.execute(
        "INSERT INTO healthdata_blood_pressure (username, datetime, systolic, diastolic) VALUES (?, ?, ?, ?)",
        (username, measured_datetime.strftime('%Y-%m-%d %H:%M:%S'), systolic, diastolic)
    )

    cursor.execute(
        "INSERT INTO healthdata_temperature (username, datetime, temperature) VALUES (?, ?, ?)",
        (username, measured_datetime.strftime('%Y-%m-%d %H:%M:%S'), temperature)
    )

# 提交更改
conn.commit()

# 关闭连接
conn.close()