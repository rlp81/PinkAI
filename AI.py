import json 
import numpy as np
from tensorflow import keras
import speech_recognition as sr
import gtts
import colorama 
colorama.init()
from audio import playaudio
from colorama import Fore, Style, Back
import random
import pickle

with open("intents.json") as file:
    data = json.load(file)
def getvoice(res):
    aud = gtts.gTTS(res)
    aud.save("aivoice.mp3")
    playaudio()
def gettext():
        r = sr.Recognizer()
        my_mic = sr.Microphone(device_index=1)
        with my_mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        return r.recognize_google(audio)

def chat():
    model = keras.models.load_model('chat_model')
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)
    max_len = 20
    while True:
        print(Fore.LIGHTBLUE_EX + f"User: " + Style.RESET_ALL, end="")
        inp = input()
        if inp.lower() == "quit":
            break
        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                             truncating='post', maxlen=max_len))
        tag = lbl_encoder.inverse_transform([np.argmax(result)])
        for i in data['intents']:
            if i['tag'] == tag:
                resp = np.random.choice(i['responses'])
                #print(Fore.LIGHTMAGENTA_EX + "Pink:" + Style.RESET_ALL , resp)
                print(Fore.LIGHTMAGENTA_EX + "Pink:" + Style.RESET_ALL,random.choice(i['responses']))
print(Fore.YELLOW + "Start messaging with the bot (type quit to stop)!" + Style.RESET_ALL)
chat()