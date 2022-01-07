import json
import os 
import numpy as np
from tensorflow import keras
import speech_recognition as sr
import gtts
import time
import colorama 
colorama.init()
from audio import playaudio
from colorama import Fore, Style, Back
import random
import pickle

class AIinfo:
    username = "Coal"
    mode = None
    modes = ["text","voice"]

with open("intents.json") as file:
    data = json.load(file)
def getvoice(res):
    aud = gtts.gTTS(res)
    aud.save("aivoice.mp3")
    try:
        playaudio()
        os.remove("aivoice.mp3")
    except:
        print("An error has occured")
        os.remove("aivoice.mp3")
def gettext():
    try:
        r = sr.Recognizer()
        my_mic = sr.Microphone(device_index=1)
        with my_mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        return r.recognize_google(audio)
    except:
        print("An error has occured")

def chat():
    print(Fore.YELLOW + "Start messaging with the bot (type quit to stop)!" + Style.RESET_ALL)
    print("Boot initiated..")
    time.sleep(1.3)
    print("Loading AI..")
    time.sleep(3)
    print("PinkAI online!")
    done = False
    while done == False:
        mode = input("What mode would you like to use? (voice/text)\n")
        if mode in AIinfo.modes:
            AIinfo.mode = mode
            done = True
        else:
            print("Please enter a valid mode!")
    model = keras.models.load_model('chat_model')
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)
    max_len = 20
    while True:
        if AIinfo.mode == "voice":
            inp = gettext()
            print(Fore.LIGHTBLUE_EX + f"User: {inp}\n" + Style.RESET_ALL, end="")
        if AIinfo.mode == "text":
            print(Fore.LIGHTBLUE_EX + f"User: " + Style.RESET_ALL, end="")
            inp = input()
        try:
            if inp.lower() == "quit":
                break
        except:
            pass
        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                             truncating='post', maxlen=max_len))
        tag = lbl_encoder.inverse_transform([np.argmax(result)])
        for i in data['intents']:
            if i['tag'] == tag:
                respp = random.choice(i['responses'])
                if i["tag"] == "love":
                    chance = random.randint(1,10000)
                    if chance == 1:
                        respp = "I love you too!"
                    else:
                        pass
                if i["tag"] == "greeting":
                    if AIinfo.username == None:
                        respp = respp[:-1]
                    else:
                        respp = respp+f" {AIinfo.username}"
                print(Fore.LIGHTMAGENTA_EX + "Pink:" + Style.RESET_ALL,respp)
                if AIinfo.mode == "voice":
                    getvoice(respp)
                try:
                    if respp.lower() == "critical error":
                        quit()
                except:
                    pass
chat()
