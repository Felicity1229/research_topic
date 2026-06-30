import os
import threading
import webbrowser
from datetime import datetime
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
RECORDINGS_DIR = 'recordings'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pc')
def index_pc():
    return render_template('index_pc.html')

@app.route('/shutdown', methods=['POST'])
def shutdown():
    threading.Timer(0.5, lambda: os._exit(0)).start()
    return jsonify({'status': 'ok'})

@app.route('/save', methods=['POST'])
def save():
    participant_id = request.form.get('participant_id', 'unknown').strip()
    filename      = request.form.get('filename', 'recording.webm')
    audio         = request.files.get('audio')

    if not audio:
        return jsonify({'status': 'error', 'message': '没有收到音频'}), 400

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = os.path.splitext(filename)
    filename  = f'{name}_{timestamp}{ext}'

    folder = os.path.join(RECORDINGS_DIR, participant_id)
    os.makedirs(folder, exist_ok=True)
    audio.save(os.path.join(folder, filename))

    return jsonify({'status': 'ok'})



if __name__ == '__main__':
    threading.Timer(1.0, lambda: webbrowser.open('http://localhost:5000/pc')).start()
    app.run(debug=False)
