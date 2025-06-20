from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import random

app = Flask(__name__)

# Simulate historical appointment data
def generate_data(n=30):
    return pd.DataFrame({
        'Patient_ID': [f'P{i+1}' for i in range(n)],
        'Requested_Time': [datetime(2025, 6, 1, random.randint(8, 15), random.randint(0, 59)) for _ in range(n)],
        'Duration_Minutes': [random.choice([10, 15, 20]) for _ in range(n)],
        'No_Show': [random.choice([0, 1]) for _ in range(n)]
    })

# Clustering
def cluster_patients(df):
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['Cluster'] = kmeans.fit_predict(df[['Duration_Minutes']])
    return df

# Scheduling Logic
def schedule(df):
    available_slots = [datetime(2025, 6, 1, hour, 0) for hour in range(8, 16)]
    schedule = []
    for _, row in df.iterrows():
        for slot in available_slots:
            new_end = slot + timedelta(minutes=row['Duration_Minutes'])
            if all(slot >= s['Scheduled_End'] or new_end <= s['Scheduled_Time'] for s in schedule):
                schedule.append({
                    'Patient_ID': row['Patient_ID'],
                    'Scheduled_Time': slot,
                    'Scheduled_End': new_end
                })
                break
    return pd.DataFrame(schedule)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book():
    data = request.json
    name = data['name']
    time = data['time']
    doctor = data['doctor']
    duration = int(data['duration'])

    # Simulate a dataset and get schedule
    df = generate_data()
    df = cluster_patients(df)
    schedule_df = schedule(df)

    # Add current booking to schedule
    schedule_df = schedule_df.append({
        'Patient_ID': name,
        'Scheduled_Time': datetime.strptime(f'2025-06-01 {time}', '%Y-%m-%d %H:%M'),
        'Scheduled_End': datetime.strptime(f'2025-06-01 {time}', '%Y-%m-%d %H:%M') + timedelta(minutes=duration)
    }, ignore_index=True)

    # Return updated schedule
    schedule_df['Scheduled_Time'] = schedule_df['Scheduled_Time'].dt.strftime('%H:%M')
    schedule_df['Scheduled_End'] = schedule_df['Scheduled_End'].dt.strftime('%H:%M')

    return jsonify(schedule_df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
