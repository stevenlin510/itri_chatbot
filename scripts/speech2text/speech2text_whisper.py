'''
OpenAI API to perform speech-to-text conversion using the "whisper-1" model. 
It takes an audio file path as input, sends a POST request to the OpenAI API, and returns the transcribed text from the audio. 
'''

import whisper
from functools import wraps
import time
model = whisper.load_model("small", device='cpu')

def measureExcutionTime(func):

    @wraps(func)
    def _time_it(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            end_ = time.time() - start
            print(f"{func.__name__} execution time: {end_: 0.4f} sec.")

    return _time_it
    
@measureExcutionTime
def speech2text(file_path):

    input_text = model.transcribe(file_path)["text"]
    
    return input_text

# WARM = speech2text('/tmp.wav')