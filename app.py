from flask import Flask, render_template, jsonify, request
import os
import random
import pyrebase
import json
import time

app = Flask(__name__)

firebase_config_path = os.path.join(os.getcwd(), 'firebase_config.json')
with open(firebase_config_path, 'r') as file:
    firebase_config = json.load(file)

firebase_storage_config_path = os.path.join(os.getcwd(), 'firebase_storage_config.json')
with open(firebase_storage_config_path, 'r') as file:
    firebase_storage_config = json.load(file)

firebase = pyrebase.initialize_app(firebase_config)
storage = firebase.storage()
db = firebase.database()

recording = False
recorded_data = []


@app.route('/')
def index():
    return render_template('index.html', storage_bucket=firebase_storage_config["storageBucket"])


@app.route('/get_random_article')
def get_random_article():
    folder_path = os.path.join(os.getcwd(), 'outputs', 'articles', 'kaktus')
    articles = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    if articles:
        random_article = random.choice(articles)
        article_path = os.path.join(folder_path, random_article)

        with open(article_path, 'r', encoding='utf-8') as file:
            content = file.read()

        return jsonify({"article": content})
    else:
        return jsonify({"article": "No articles available."})


@app.route('/start_recording', methods=['POST'])
def start_recording():
    global recording
    global recorded_data

    recording = True
    recorded_data = []
    return jsonify({"status": "Recording started"})


@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    global recording
    global recorded_data

    recording = False
    try:
        if recorded_data:
            # Сохраняем запись в Firebase Storage
            timestamp = int(time.time())

            # Итерируем по всем записанным данным и сохраняем их в Firebase Storage
            for i, audio_data in enumerate(recorded_data):
                storage.child(f'recordings/recording_{timestamp}_{i + 1}.wav').put(audio_data)

            # Очищаем recorded_data для следующей записи
            recorded_data = []

            return jsonify({"status": "Recording stopped", "success": True})
        else:
            return jsonify({"status": "No recorded data to stop", "success": False})
    except Exception as e:
        return jsonify({"status": "Failed to stop recording", "success": False, "error": str(e)})


@app.route('/record_data', methods=['POST'])
def record_data():
    global recording
    global recorded_data

    if recording:
        data = request.get_json()
        print('Received Data:', data)
        recorded_data.append(data['audioData'])
        return jsonify({"status": "Data recorded"})
    else:
        return jsonify({"status": "Not recording"})

@app.route('/get_recording_status', methods=['GET'])
def get_recording_status():
    global recording
    return jsonify({"recording": recording})


def record_data():
    global recording
    global recorded_data

    if recording:
        data = request.get_json()
        recorded_data.append(data['audioData'])
        print('Recorded data:', recorded_data)  # Отладочный вывод
        return jsonify({"status": "Data recorded"})
    else:
        return jsonify({"status": "Not recording"})


@app.route('/send_to_firebase', methods=['POST'])
def send_to_firebase():
    try:
        data = request.get_json()
        audio_data = data['audioData']
        timestamp = int(time.time())

        # Загружаем файл в Firebase Storage
        file_path = f'recordings/recording_{timestamp}.wav'
        storage.child(file_path).put(audio_data)
        print('Recording sent to Firebase:', file_path)  # Отладочный вывод

        return jsonify({"status": "Recording sent to Firebase", "success": True, "timestamp": timestamp})
    except Exception as e:
        return jsonify({"status": "Failed to send recording to Firebase", "success": False, "error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)
