import sqlite3

# 连接到数据库
conn = sqlite3.connect('TheHealthData.db')#我在想要不要把这几个分开写，但根据没必要，这个其实没有创建的话会自己创建

# 执行 SQL 语句对象，这个叫游标
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
    FOREIGN KEY (username) REFERENCES user(username)
);
''')#这几个的外键都是username，而且python的注释不能写到execute里面

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

# #插入一些数据，用过了现在给他注释掉
# cursor.execute("INSERT INTO user (username, password) VALUES ('user1', '123456')")
# cursor.execute("INSERT INTO user (username, password) VALUES ('user2', '123456')")
#
# cursor.execute("INSERT INTO healthdata_heart_rate (username, heart_rate) VALUES ('user1', 80)")
# cursor.execute("INSERT INTO healthdata_heart_rate (username, heart_rate) VALUES ('user2', 75)")
#
#
# cursor.execute("INSERT INTO healthdata_blood_pressure (username, systolic, diastolic) VALUES ('user1', 120, 80)")
# cursor.execute("INSERT INTO healthdata_blood_pressure (username, systolic, diastolic) VALUES ('user2', 130, 85)")
#
# cursor.execute("INSERT INTO healthdata_temperature (username, temperature) VALUES ('user1', 36.5)")
# cursor.execute("INSERT INTO healthdata_temperature (username, temperature) VALUES ('user2', 36.8)")

# 提交事务
conn.commit()

# 关闭连接
conn.close()
