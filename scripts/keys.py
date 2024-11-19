from api_keys_n_variables import openai_api_key, azure_speech_key, azure_service_region
from api_keys_n_variables import QDRANT_URL, QDRANT_API_KEY, collection_name, SERPER_API_KEY
from path_hold import usd_scene, unreal_exe_path
from path_hold import try_again_female_voice, try_again_male_voice
import os

openai_api_key = openai_api_key

azure_speech_key = azure_speech_key
azure_service_region = azure_service_region

usd_scene = usd_scene
unreal_exe_path = unreal_exe_path

try_again_female_voice = try_again_female_voice
try_again_male_voice = try_again_male_voice

server = 'http://localhost:8011'
player = "/World/audio2face/Player"  # Your audio2face player
fullface_core = "/World/audio2face/CoreFullface"  # Your Player Instance

a2f_url = 'localhost:50051'  # The audio2face URL by default
a2f_avatar_instance = "/World/audio2face/PlayerStreaming"  # The instance name of the avatar in a2f

os.environ['QDRANT_URL'] = QDRANT_URL
os.environ['QDRANT_API_KEY'] = QDRANT_API_KEY
collection_name = collection_name
QDRANT_URL = QDRANT_URL
QDRANT_API_KEY = QDRANT_API_KEY
os.environ["SERPER_API_KEY"] = SERPER_API_KEY

female_voice = "zh-TW-HsiaoChenNeural"
female_default_speaking_emotion = {
    "a2f_instance": fullface_core,
    "emotions": {
        "neutral": 0.2,
        "amazement": 0.1,
        "anger": 0,
        "cheekiness": 0,
        "disgust": 0,
        "fear": 0,
        "grief": 0,
        "joy": 0.7,
        "outofbreath": 0,
        "pain": 0,
        "sadness": 0,
    }
}

male_voice = "zh-TW-YunJheNeural"
male_default_speaking_emotion = {
    "a2f_instance": fullface_core,
    "emotions": {
        "neutral": 0.2,
        "amazement": 0.1,
        "anger": 0,
        "cheekiness": 0,
        "disgust": 0,
        "fear": 0,
        "grief": 0,
        "joy": 0.7,
        "outofbreath": 0,
        "pain": 0,
        "sadness": 0,
    }
}
