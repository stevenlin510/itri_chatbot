'''
Handle setting up and managing the configuration through OSC (Open Sound Control) messages
'''

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from ..record_user_audio.record_audio_from_user import RecordAudio

record_audio_instance = RecordAudio()

class BotSetup:
    def __init__(self):
        self.gender = None
        self.recorded = False
        self.end = False
        
    def set_gender(self, new_gender):
        self.gender = new_gender

    def get_gender(self):
        return self.gender

    def set_recorded(self, new_recorded):
        self.stop_record = new_recorded

    def get_recorded(self):
        return self.recorded

    def set_end(self, new_end):
        self.end = new_end

    def get_end(self):
        return self.end
        

    # Define a function to handle incoming OSC messages
    def handle_message(self, address, *args):
        if address.startswith("/Male"):
            # Check if the OSC message contains any float values
            float_args = [arg for arg in args if isinstance(arg, float)]
            if len(float_args) > 0:
                received_float = float_args[0]  # Use the first float value
                print(f"Received float value for {address}: {received_float}")
                self.set_gender('m')
                print(self.get_gender())
            else:
                print(f"Received an unexpected message for {address}: {args}")
        elif address.startswith("/Female"):
            float_args = [arg for arg in args if isinstance(arg, float)]
            if len(float_args) > 0:
                received_float = float_args[0] 
                print(f"Received float value for {address}: {received_float}")
                self.set_gender('f')
                print(self.get_gender())
            else:
                print(f"Received an unexpected message for {address}: {args}")
        elif address.startswith("/StartRecord"):
            float_args = [arg for arg in args if isinstance(arg, float)]
            if len(float_args) > 0:
                received_float = float_args[0] 
                print(f"Received float value for {address}: {received_float}")
                record_audio_instance.start_recording()
            else:
                print(f"Received an unexpected message for {address}: {args}")
        elif address.startswith("/StopRecord"):
            float_args = [arg for arg in args if isinstance(arg, float)]
            if len(float_args) > 0:
                received_float = float_args[0]
                print(f"Received float value for {address}: {received_float}")
                record_audio_instance.stop_recording_and_save()
                self.set_recorded(True)
            else:
                print(f"Received an unexpected message for {address}: {args}")
        elif address.startswith("/End"):
            float_args = [arg for arg in args if isinstance(arg, float)]
            if len(float_args) > 0:
                received_float = float_args[0]
                print(f"Received float value for {address}: {received_float}")
                print("Attempting to exit the script")
                self.set_end(True)
            else:
                print(f"Received an unexpected message for {address}: {args}")
        else:
            # Handle other unexpected messages
            print(f"Received an unexpected message: {address} {args}")

    # Set up and start a UDP server to listen for incoming OSC messages
    def setup_udp_server(self):
        # Set up the dispatcher to associate the incoming addresses with the handling function
        dispatcher = Dispatcher()
        dispatcher.map("/Male", self.handle_message)    # Handle "/Test" messages
        dispatcher.map("/Female", self.handle_message)   # Handle "/Test2" messages
        dispatcher.map("/StartRecord", self.handle_message)    # Handle "/Send" messages
        dispatcher.map("/StopRecord", self.handle_message)  # Handle "/Choose" messages
        dispatcher.map("/End", self.handle_message)  # Handle "/Choose" messages
        # Add more mappings for other message addresses as needed

        # Set up the UDP server to listen on 127.0.0.1:5007 and use the dispatcher to handle incoming messages
        server = BlockingOSCUDPServer(("127.0.0.1", 5007), dispatcher)
        print("UDP Server listening on 127.0.0.1:5007...")

        # Start the server to begin listening for incoming messages
        server.serve_forever()
        return server