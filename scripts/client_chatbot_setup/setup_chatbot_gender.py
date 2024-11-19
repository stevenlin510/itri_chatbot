'''
Defines a Python class named BotGenderSetup.
The class is responsible for configuring various aspects of the bot's behavior based on the specified gender. 
It sets up attributes related to voice files, speaking emotions, and retry prompts for different genders.
'''

from ..keys import female_voice, male_voice
from ..keys import try_again_male_voice, try_again_female_voice
from ..keys import female_default_speaking_emotion, male_default_speaking_emotion


class BotGenderSetup:
    def __init__(self):
        self.voice_name = None
        self.default_speaking_emotion = None
        self.try_again_voice_file = None

    def setup_bot_gender(self, gender):
        if gender == 'm':
            self.voice_name = male_voice
            self.default_speaking_emotion = male_default_speaking_emotion
            self.try_again_voice_file = try_again_male_voice
        elif gender == 'f':
            self.voice_name = female_voice
            self.default_speaking_emotion = female_default_speaking_emotion
            self.try_again_voice_file = try_again_female_voice
        return True

    def get_voice_name(self):
        return self.voice_name

    def get_default_speaking_emotion(self):
        return self.default_speaking_emotion

    def get_try_again_voice_file(self):
        return self.try_again_voice_file