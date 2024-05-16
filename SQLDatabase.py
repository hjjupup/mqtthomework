import sqlite3

# 连接到数据库
conn = sqlite3.connect('HealthData.db')#我在想要不要把这几个分开写，但根据没必要

# 执行 SQL 语句对象
cursor = conn.cursor()

# 创建 user 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
);
''')

# 创建 healthdata_heart_rate 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS healthdata_heart_rate (
    username TEXT,
    heart_rate INT,
    FOREIGN KEY (username) REFERENCES user(username) #这几个的外键都是username
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS healthdata_blood_pressure (
    username TEXT,
    systolic INT,
    diastolic INT,
    FOREIGN KEY (username) REFERENCES user(username)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS healthdata_temperature (
    username TEXT,
    temperature REAL,
    FOREIGN KEY (username) REFERENCES user(username)
);
''')

# 提交事务
conn.commit()

# 关闭连接
conn.close()