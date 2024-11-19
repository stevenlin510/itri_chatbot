import azure.cognitiveservices.speech as speechsdk
import numpy as np
from scripts.client_chatbot_setup.display_w_unreal_n_audio2face import push_audio_file_npdata

class azure_TTS():

    def __init__(self, voice, azure_speech_key, azure_service_region):

        self.file_name = 'tmp.wav'
        audio_config = speechsdk.audio.AudioOutputConfig(
            filename=self.file_name)
        speech_config = speechsdk.SpeechConfig(subscription=azure_speech_key,
                                               region=azure_service_region)
        speech_config.speech_synthesis_voice_name = voice
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=audio_config)

    def text_to_speech(self, text):

        result = self.speech_synthesizer.speak_text_async(text).get()
        audio_data_int16 = np.frombuffer(result.audio_data, dtype=np.int16)
        audio_data_float32 = audio_data_int16.astype(np.float32) / 32768.0
        audio_data_float32 = audio_data_float32[700:]
        push_audio_file_npdata(audio_data_float32)
