import sqlite3
from turtle import pd
from IPython.display import display
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd
import time

def calculate_and_set_ylim(ax, systolics, diastolics):
    # Set the y-axis limit based on the minimum value of systolics and diastolics
    min_value = min(min(systolics), min(diastolics))
    ax.set_ylim(min_value - 20, None)#set the size of bp因为bp的线有两条，我让图好看点在下面预留了点空间

def visu_user_data(username):
    # Connect to the database
    conn = sqlite3.connect('TheHealthData.db')
    cursor = conn.cursor()

    # Retrieve data for the given username
    cursor.execute('SELECT datetime, heart_rate FROM healthdata_heart_rate WHERE username=?', (username,))
    heart_rates = cursor.fetchall()

    cursor.execute('SELECT datetime, systolic, diastolic FROM healthdata_blood_pressure WHERE username=?', (username,))
    blood_pressures = cursor.fetchall()

    cursor.execute('SELECT datetime, temperature FROM healthdata_temperature WHERE username=?', (username,))
    temperatures = cursor.fetchall()

    conn.close()

    fig, ax = plt.subplots(3, 1, figsize=(10, 15))

    # Heart rate data
    times_hr = [datetime.strptime(item[0], '%Y-%m-%d %H:%M:%S') for item in heart_rates]
    rates = [item[1] for item in heart_rates]

    if times_hr and rates:
        ax[0].plot(times_hr, rates, marker='o', linestyle='-', color='blue')

        ax[0].fill_between(times_hr, rates, 100, where=[r > 100 for r in rates], color='red', alpha=0.3)
        ax[0].fill_between(times_hr, rates, 60, where=[r < 60 for r in rates], color='green', alpha=0.3)

        ax[0].set_title(f'{username} - Heart Rate')
        ax[0].set_ylabel('Beats per Minute')
        ax[0].axhline(100, linestyle='--', color='red', label='High HR Alert (100 BPM)')
        ax[0].axhline(60, linestyle='--', color='green', label='Low HR Alert (60 BPM)')
        ax[0].legend()

    # Blood pressure data
    times_bp = [datetime.strptime(item[0], '%Y-%m-%d %H:%M:%S') for item in blood_pressures]
    systolics = [item[1] for item in blood_pressures]
    diastolics = [item[2] for item in blood_pressures]

    if times_bp and systolics and diastolics:
        ax[1].plot(times_bp, systolics, marker='s', linestyle='-', color='orange', label='Systolic')
        ax[1].plot(times_bp, diastolics, marker='s', linestyle='-', color='purple', label='Diastolic')

        ax[1].fill_between(times_bp, systolics, 140, where=[s > 140 for s in systolics], color='red', alpha=0.3)
        ax[1].fill_between(times_bp, diastolics, 90, where=[d > 90 for d in diastolics], color='red', alpha=0.3)
        ax[1].fill_between(times_bp, systolics, 90, where=[s < 90 for s in systolics], color='green', alpha=0.3)
        ax[1].fill_between(times_bp, diastolics, 60, where=[d < 60 for d in diastolics], color='green', alpha=0.3)

        ax[1].set_title(f'{username} - Blood Pressure')
        ax[1].axhline(140, linestyle='--', color='red', label='High BP Alert (140/90 mmHg)')
        ax[1].axhline(90, linestyle='--', color='red')
        ax[1].axhline(90, linestyle='--', color='green', label='Low BP Alert (90/60 mmHg)')
        ax[1].axhline(60, linestyle='--', color='green')
        ax[1].legend()

        calculate_and_set_ylim(ax[1], systolics, diastolics)

    # Temperature data
    times_temp = [datetime.strptime(item[0], '%Y-%m-%d %H:%M:%S') for item in temperatures]
    temps = [item[1] for item in temperatures]

    if times_temp and temps:
        ax[2].plot(times_temp, temps, marker='o', linestyle='-', color='purple')

        ax[2].fill_between(times_temp, temps, 38, where=[t > 38 for t in temps], color='red', alpha=0.3)
        ax[2].fill_between(times_temp, temps, 36, where=[t < 36 for t in temps], color='green', alpha=0.3)

        ax[2].set_title(f'{username} - Temperature')
        ax[2].axhline(38, linestyle='--', color='red', label='High Temp Alert (38°C)')
        ax[2].axhline(36, linestyle='--', color='green', label='Low Temp Alert (36°C)')
        ax[2].legend()

    plt.tight_layout()#自动调整间距，但有没有好像都没区别
    plt.savefig(f'{username}_health_data_chart.png')

def color_alert(val):#https://deepinout.com/pandas/pandas-questions/962_pandas_how_to_use_pandas_stylers_for_coloring_an_entire_row_based_on_a_given_column.html
    #这个本来是想和下面那个打印一起搞做颜色的区分的，但是有问题，要有连续的两个点或者以上才会有颜色的填充
    color = 'red' if val == 'High' else 'green' if val == 'Low' else 'black'
    return f'color: {color}'

def print_user_data(username):
    conn = sqlite3.connect('TheHealthData.db')
    cursor = conn.cursor()

    cursor.execute('SELECT datetime, heart_rate FROM healthdata_heart_rate WHERE username=?', (username,))
    heart_rates = cursor.fetchall()

    cursor.execute('SELECT datetime, systolic, diastolic FROM healthdata_blood_pressure WHERE username=?', (username,))
    blood_pressures = cursor.fetchall()

    cursor.execute('SELECT datetime, temperature FROM healthdata_temperature WHERE username=?', (username,))
    temperatures = cursor.fetchall()

    conn.close()

    heart_rate_data = [(item[0], item[1], 'High' if item[1] > 100 or item[1] < 60 else 'Normal') for item in heart_rates]
    blood_pressure_data = [(item[0], item[1], item[2], 'High' if item[1] > 140 or item[2] > 90 or item[1] < 90 or item[2] < 60 else 'Normal') for item in blood_pressures]
    temperature_data = [(item[0], item[1], 'High' if item[1] > 38 or item[1] < 36 else 'Normal') for item in temperatures]

    hr_df = pd.DataFrame(heart_rate_data, columns=['Data_Time', 'Heart Rate', 'Status'])
    bp_df = pd.DataFrame(blood_pressure_data, columns=['Data_Time', 'Systolic', 'Diastolic', 'Status'])
    temp_df = pd.DataFrame(temperature_data, columns=['Data_Time', 'Temperature', 'Status'])

    print("Heart Rate Data:")
    display(hr_df)
    print("\nBlood Pressure Data:")
    display(bp_df)
    print("\nTemperature Data:")
    display(temp_df)

start_time = time.time()
conn = sqlite3.connect('TheHealthData.db')
cursor = conn.cursor()

cursor.execute("SELECT username, datetime, heart_rate FROM healthdata_heart_rate ORDER BY username, datetime")
heart_rates = cursor.fetchall()

cursor.execute("SELECT username, datetime, systolic, diastolic FROM healthdata_blood_pressure ORDER BY username, datetime")
blood_pressures = cursor.fetchall()

cursor.execute("SELECT username, datetime, temperature FROM healthdata_temperature ORDER BY username, datetime")
temperatures = cursor.fetchall()

conn.close()

usernames = set([item[0] for item in heart_rates])

for username in usernames:
    visu_user_data(username)

end_time = time.time()
execution_time = end_time - start_time
print("Execution time: {:.2f} seconds".format(execution_time))
