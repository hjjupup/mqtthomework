import sqlite3
import pandas as pd
import plotly.graph_objects as go#reference:https://blog.csdn.net/wzk4869/article/details/129864811
from plotly.subplots import make_subplots
from datetime import datetime

#这个是用别的可视化库写的，但是我的没有写对应的传html文件的函数，而且html函数的打开方式不一样
def visu_user_data_plotly(username):
    #和另一个visu_user_data一样的准备数据
    conn = sqlite3.connect('TheHealthData.db')
    cursor = conn.cursor()

    #检索数据
    cursor.execute('SELECT datetime, heart_rate FROM healthdata_heart_rate WHERE username=?', (username,))
    heart_rates = cursor.fetchall()

    cursor.execute('SELECT datetime, systolic, diastolic FROM healthdata_blood_pressure WHERE username=?', (username,))
    blood_pressures = cursor.fetchall()

    cursor.execute('SELECT datetime, temperature FROM healthdata_temperature WHERE username=?', (username,))
    temperatures = cursor.fetchall()

    conn.close()

    #准备数据并且用key时间排序，不然最后的的图标是按照高低排序的
    heart_rates = sorted(heart_rates, key=lambda x: datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S'))
    blood_pressures = sorted(blood_pressures, key=lambda x: datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S'))
    temperatures = sorted(temperatures, key=lambda x: datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S'))

    times_hr = [datetime.strptime(item[0], '%Y-%m-%d %H:%M:%S') for item in heart_rates]
    rates = [item[1] for item in heart_rates]

    times_bp = [datetime.strptime(item[0], '%Y-%m-%d %H:%M:%S') for item in blood_pressures]
    systolics = [item[1] for item in blood_pressures]
    diastolics = [item[2] for item in blood_pressures]

    times_temp = [datetime.strptime(item[0], '%Y-%m-%d %H:%M:%S') for item in temperatures]
    temps = [item[1] for item in temperatures]

    fig = make_subplots(rows=3, cols=1, subplot_titles=('Heart Rate', 'Blood Pressure', 'Temperature'))

    # Heart rate plot
    if times_hr and rates:
        fig.add_trace(go.Scatter(x=times_hr, y=rates, mode='lines+markers', name='Heart Rate'), row=1, col=1)
        fig.add_trace(go.Scatter(x=times_hr, y=[100] * len(times_hr), mode='lines', name='High HR Alert (100 BPM)', line=dict(dash='dash', color='red')), row=1, col=1)
        fig.add_trace(go.Scatter(x=times_hr, y=[60] * len(times_hr), mode='lines', name='Low HR Alert (60 BPM)', line=dict(dash='dash', color='green')), row=1, col=1)

    # Blood pressure plot
    if times_bp and systolics and diastolics:
        fig.add_trace(go.Scatter(x=times_bp, y=systolics, mode='lines+markers', name='Systolic'), row=2, col=1)
        fig.add_trace(go.Scatter(x=times_bp, y=diastolics, mode='lines+markers', name='Diastolic'), row=2, col=1)
        fig.add_trace(go.Scatter(x=times_bp, y=[60] * len(times_bp), mode='lines', name='Low BP Alert (60 mmHg)',line=dict(dash='dash', color='green')), row=2, col=1)
        fig.add_trace(go.Scatter(x=times_bp, y=[140] * len(times_bp), mode='lines', name='High BP Alert (140 mmHg)', line=dict(dash='dash', color='red')), row=2, col=1)
        fig.add_trace(go.Scatter(x=times_bp, y=[90] * len(times_bp), mode='lines', name='High BP Alert (90 mmHg)',line=dict(dash='dash', color='red')), row=2, col=1)
        fig.add_trace(go.Scatter(x=times_bp, y=[90] * len(times_bp), mode='lines', name='Low BP Alert (90 mmHg)', line=dict(dash='dash', color='green')), row=2, col=1)

    # Temperature plot
    if times_temp and temps:
        fig.add_trace(go.Scatter(x=times_temp, y=temps, mode='lines+markers', name='Temperature'), row=3, col=1)
        fig.add_trace(go.Scatter(x=times_temp, y=[38] * len(times_temp), mode='lines', name='High Temp Alert (38°C)', line=dict(dash='dash', color='red')), row=3, col=1)
        fig.add_trace(go.Scatter(x=times_temp, y=[36] * len(times_temp), mode='lines', name='Low Temp Alert (36°C)', line=dict(dash='dash', color='green')), row=3, col=1)

    #这个有点像html的格式
    fig.update_layout(
        height=800,
        width=1000,
        title_text=f'{username} - Health Data',
        showlegend=True,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="LightSteelBlue",
        legend=dict(
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top"
        )

    )

    fig.update_xaxes(title_text="Time", row=1, col=1)
    fig.update_xaxes(title_text="Time", row=2, col=1)
    fig.update_xaxes(title_text="Time", row=3, col=1)

    fig.update_yaxes(title_text="BPM", row=1, col=1)
    fig.update_yaxes(title_text="mmHg", row=2, col=1)
    fig.update_yaxes(title_text="°C", row=3, col=1)


    fig.write_html(f'{username}_health_data_chart.html')


visu_user_data_plotly('user1')