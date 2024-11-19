import os
from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from scipy.io.wavfile import write
import base64
import numpy as np
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import pyaudio
import whisper
from flask_socketio import SocketIO, emit
import paho.mqtt.client as mqtt

mqtt_broker = 'localhost'
mqtt_port = 1883
# 設定 MQTT 客戶端
client = mqtt.Client()
client.connect(mqtt_broker, mqtt_port, 60)
client.subscribe("user_text")
# client.subscribe("finish_talking")
client.loop_start()


model_w = whisper.load_model('small')

app = Flask(__name__)
socketio = SocketIO(app)
is_recording = True

# def on_message(client, userdata, msg):
#     global messages, messages_comming
#     topic = msg.topic
#     payload = msg.payload.decode()
    
#     # 檢查接收到的主題是否是 'user_text'
#     if topic == 'finish_talking':
#         print(payload)
#         # print(f"Received message on topic '{topic}': {payload}")
#         if payload == 'True':
#             print('Answer is Finished, Start next recodring.')
#             socketio.emit('start_recording')
#         else:
#             print('System is answering, stop recording.')
#             socketio.emit('stop_recording')

# client.on_message = on_message

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stop_and_run_script', methods=['POST'])
def handle_audio_data():
    file_path = 'user_audio.wav'
    try:  
        audio_file = request.files['audio']
        audio_file.save(file_path)

        
        result_w = model_w.transcribe(file_path, fp16=False)
        message_to_publish= result_w['text']
        print(message_to_publish)

   
        client.publish('user_text', message_to_publish)

        # 傳送資料
        
        return 'Audio recorded and Python script executed successfully!'
    
    except Exception as e:
        return f'Error: {e}'

# # 前端连接成功后，发送当前录音状态
# @socketio.on('connect')
# def handle_connect():
#     print('開始錄音')
#     emit('recording_status', is_recording)

# # 前端发起开始录音的请求
# @socketio.on('start_recording')
# def handle_start_recording():
#     global is_recording
#     is_recording = True
#     print('往前端送出開始錄音')
#     emit('recording_status', is_recording)

# # 前端发起停止录音的请求
# @socketio.on('stop_recording')
# def handle_stop_recording():
#     global is_recording
#     is_recording = False
#     print('往前端送出停止錄音')
#     emit('recording_status', is_recording)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=88)
