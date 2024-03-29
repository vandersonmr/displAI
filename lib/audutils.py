import speech_recognition as sr
import gtts
from pydub import AudioSegment
from pydub.playback import play
import os
from io import BytesIO
import pygame

class AudioHelper:
    def __init__(self):
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()
        with self.mic as source:
            self.r.adjust_for_ambient_noise(source)
        # r.pause_threshold = 0.7
        # r.operation_timeout = 0.5
        self.r.dynamic_energy_threshold = True

    def listen(self):
        with self.mic as source:
            audio = self.r.listen(source, timeout=10)
        return audio

    def transcript(self, raudio):
        #print(raudio)
        rtxt = None
        try:
            rtxt = self.r.recognize_google(raudio)
        except sr.UnknownValueError:
            print("Could not understand audio, please say again.")

        except sr.RequestError as e:
            print("Could not request audio transcription ")
        return rtxt

    def parser_w_detect(self, raud, keywords):
        try:
            rtxt = self.transcript(raud)
            kw_det = False
            for kw in keywords:
                if kw.casefold() in rtxt.casefold():
                    kw_det = True  # keyword detected.
                    #rcmd = rtxt.casefold().strip(kw.casefold())  # received command
                    print(f"Keyword detected:{kw}, processing:{rcmd}")
                    break
            if kw_det:
                return kw_det, rtxt, rcmd
            else:
                return False, rtxt, None

        except sr.UnknownValueError:
            print("Could not understand audio, please say again.")

        except sr.RequestError as e:
            print("Could not request audio transcription ")

    def say(self, txt, lang="en", accent="us", path=''):
        aud = gtts.gTTS(txt, lang=lang, tld=accent)

        fp = BytesIO()
        aud.write_to_fp(fp)
        fp.seek(0)

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  
