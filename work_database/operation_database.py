#这段主要写的就是on_message用来接收处理message，之后会根据message去操作database，还有图片的传输函数
import mysql.connector
import sqlite3
import base64


#topic的大致结构healthdata/user_id/operation_type/data_type/data_value/data_time
# cmnd_topic="house/cmnd/#"#用于发送命令给设备的主题
# response_topic="house/response/"#接收设备响应的主题
# connected_topic="house/connected/"#设备连接状态的主题
# status_topic="house/status/"#设备状态信息的主题
#计划加上一个命名空间是manager的，看到时候有没有空
group_names = ["heart_rata", "blood_pressure", "temperature"]

# 连接到 MySQL 服务器，蛮多参数要改 connect to sql，some agruments need be charged
mydb = mysql.connector.connect(
    host="localhost",    # 数据库主机地址
    user="root",         # 数据库用户名
    password="jiejiewoaini0",  # 数据库密码，
    database="TheHealthData"    # 数据库名称
)

# 创建一个游标对象
conn = sqlite3.connect('TheHealthData.db')
cursor = mydb.cursor()

def on_message(client,userdata, msg):#成功连接的时候调用的
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))#处理过后的msg
    message_handler(client,topic,m_decode)

def message_handler(client,topic,msg):
    #我这个是根据week8中的device.py改的，我有点奇怪topic不应该没有数据的具体信息吗，具体的信息在payload中
    topics=topic.split("/")
    topic_len= len(topics)
    sensor_name = topics[3]
    print("command for device ", sensor_name)
    #目前没看懂这部分在干嘛
    # ret = check_name(sensor_name)
    # if not ret:
    #     return
    # topic的大致结构healthdata/user_id/operation_type/data_type/data_value/data_time
    if topic_len == 2:#针对可视化的message_hander
        user_id = topics[1]
        publish_chart(user_id,client)
    if topic_len == 4:
        operation_type=topics[2]
        if operation_type=='query_data':
            user_id = topics[1]
            data_type = topics[3]
            query_data(user_id, data_type)
    if topic_len == 6:
        data_value = topics[4]
        # print("command value is ", data_value)
        operation_type = topics[2]
        user_id = topics[1]
        data_type = topics[3]
        data_time = topic[5]
        if operation_type=='insert_data':
            insert_data(user_id,data_time,data_value,data_type)
        if operation_type=='delete_data':
            delete_data(user_id,data_time,data_type)
        if operation_type=='update_data':
            update_data(user_id,data_time,data_value,data_type)

        # update_status(client,sensor_name,command_value)
        #send_response(client,sensor_name,command_value)

def check_name(sensor_name):
    match_flag=False
    for i in range(len(group_names)):
        if sensor_name==group_names[i]:
            print("sensor group name match " +sensor_name)
            match_flag=True
            break
    return match_flag
#首先是增删查改，这个是3个data_type都一起用的
def insert_data(username, datetime, value, data_type):
    if data_type not in ["heart_rates", "blood_pressures", "temperatures"]:
        raise ValueError("Invalid data type")#输入检测

    table_name = f"healthdata_{data_type}"
    cursor.execute(f'''
    INSERT INTO {table_name} (username, datetime, value)
    VALUES (?, ?, ?)
    ''', (username, datetime, value))
    conn.commit()

def delete_data(username, datetime, data_type):
    if data_type not in ["heart_rates", "blood_pressures", "temperatures"]:
        raise ValueError("Invalid data type")

    table_name = f"healthdata_{data_type}"
    cursor.execute(f'''
    DELETE FROM {table_name}
    WHERE username=? AND datetime=?
    ''', (username, datetime))
    conn.commit()

def query_data(username, data_type):
    if data_type not in ["heart_rates", "blood_pressures", "temperatures"]:
        raise ValueError("Invalid data type")

    table_name = f"healthdata_{data_type}"
    cursor.execute(f'''
    SELECT * FROM {table_name} WHERE username=?
    ''', (username,))
    return cursor.fetchall()

def update_data(username, datetime, new_value, data_type):
    if data_type not in ["heart_rates", "blood_pressures", "temperatures"]:
        raise ValueError("Invalid data type")

    table_name = f"healthdata_{data_type}"
    cursor.execute(f'''
    UPDATE {table_name}
    SET value=?
    WHERE username=? AND datetime=?
    ''', (new_value, username, datetime))
    conn.commit()

#传输可视化的函数
def publish_chart(username, client):
    image_file = f'{username}_health_data_chart.png'
    try:
        with open(image_file, 'rb') as f:
            image_data = f.read()
            #将图片转换为base64编码
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            client.connect('localhost', 1883)
            client.publish('image_topic', image_base64)
            # 断开连接
            client.disconnect()
    except FileNotFoundError:
        print(f'Chart image file not found for {username}')



