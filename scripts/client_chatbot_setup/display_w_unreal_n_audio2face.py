'''
Communicates with an Unreal Engine-based application using OSC (Open Sound Control) messages
'''
import requests, subprocess, soundfile
from pythonosc import udp_client
from ..audio2face_source_code.audio2face_streaming_utils import push_audio_track
from ..keys import server, usd_scene, a2f_avatar_instance, a2f_url, unreal_exe_path

# This creates a UDP client object for sending OSC messages to the IP address '127.0.0.1' (localhost) on port 5008.
client = udp_client.SimpleUDPClient('127.0.0.1', 5008)


# This function is presumably meant to open an Unreal Engine executable. The subprocess.Popen call opens the executable as a new process.
def open_unreal_exe():
    exe_path = unreal_exe_path
    subprocess.Popen(
        [exe_path],
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


# This function interact with audio2face application that connects audio inputs and facial animation. It performs the following steps
def A2F():
    #Sends a POST request to load a USD scene
    data = {"file_name": usd_scene}
    #Sends a POST request to set the number of animation keys in the application using the a2f_avatar_instance.
    requests.post(f'{server}/A2F/USD/Load', json=data).json

    print("Loaded!")
    #Retrieves instances of an A2F (Audio to Face) animation from the server.
    data = {"a2f_instance": a2f_avatar_instance}
    requests.post(f'{server}/A2F/POST/NumKeys', json=data).json()

    a2f_instance = requests.get(f'{server}' + "/A2F/GetInstances").json
    print(f'A2F Instance: {a2f_instance}')
    return a2f_instance


# This function sends a message to set the facial expression to the default emotion.
def set_to_default_emotion():
    client.send_message("/FaceIdle", float(0))


# This function sends a POST request to set an emotion in the A2F application based on the provided JSON data.
def push_emotion(json):
    requests.post(f'{server}/A2F/A2E/SetEmotionByName', json=json)


# This function reads the converted audio file, sends a message to set the facial expression to an idle state, and then pushes the audio data to the A2F.
def push_audio_file(converted_output_filename):
    data, samplerate = soundfile.read(converted_output_filename,
                                      dtype="float32")
    client.send_message("/FaceIdle", float(1))
    push_audio_track(a2f_url, data, samplerate, a2f_avatar_instance)


# This function reads the converted audio file, sends a message to set the facial expression to an idle state, and then pushes the audio data to the A2F.
def push_audio_file_npdata(data, samplerate=16000):
    client.send_message("/FaceIdle", float(1))
    push_audio_track(a2f_url, data, samplerate, a2f_avatar_instance)


# This function sends a message to close the A2F application and the Unreal Engine executable.
def close_audio2face_n_unreal():
    client.send_message("/FaceIdle", float(2))


def show_record_message():
    client.send_message("/StartRecord", float(3))


def wait_a_min():
    client.send_message("/Wait", float(4))


def print_prompt(text):
    client.send_message("/UserPrompt", text)


def gpt_response(text):
    client.send_message("/GptResponse", text)