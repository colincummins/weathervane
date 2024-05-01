from gtts import gTTS
from playsound import playsound

class VoiceAPI:
    def __init__(self):
        pass

    def say_quote(self, body, author):
        for item in [body, author]:
            tts = gTTS(item,lang="en")
            tts.save('audio.mp3')
            playsound('audio.mp3')
