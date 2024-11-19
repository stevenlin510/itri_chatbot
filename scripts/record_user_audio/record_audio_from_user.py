'''
This code defines a class named RecordAudio that is designed to handle audio recording using the PyAudio library in Python. 
The class provides methods for starting and stopping audio recording, as well as saving the recorded audio to a WAV file. 
'''

import pyaudio, wave, threading

class RecordAudio:
    def __init__(self):
        self.recording_thread = None
        self.stop_event = None
        self.stream = None
        self.frames = []
        self.output_file = "./scripts/record_user_audio/saved_temp_audio_file/recorded_audio.wav"  # Change this to the desired output file path
        self.audio = None  # Declare audio in the global scope

    # Function to start recording
    def start_recording(self):
        if self.recording_thread is None or not self.recording_thread.is_alive():
            self.stop_event = threading.Event()
            self.frames = []
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=44100,
                                input=True,
                                frames_per_buffer=1024)
            self.recording_thread = threading.Thread(target=self._record_audio, args=(self.stop_event,))
            self.recording_thread.start()
            print("Recording started...")

    # Function to stop recording and save the audio
    def stop_recording_and_save(self):
        if self.recording_thread and self.recording_thread.is_alive():
            self.stop_event.set()
            self.recording_thread.join()
            self.stop_event = None
            self.recording_thread = None

            # Stop the audio stream and terminate PyAudio
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None
            if self.audio:
                self.audio.terminate()
                self.audio = None

            # Save the recorded audio to a WAV file
            self.save_audio(self.output_file, self.frames)
            print(f"Audio saved to {self.output_file}")

    # Internal function for recording audio
    def _record_audio(self, stop_event):
        while not stop_event.is_set():
            data = self.stream.read(1024)
            self.frames.append(data)

    # Function to save the audio frames to a WAV file
    def save_audio(self, output_file, frames):
        wf = wave.open(output_file, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)  # Use a fixed sample width of 2 bytes (16-bit)
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()