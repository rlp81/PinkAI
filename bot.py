import discord
from discord.ext import commands
import random
import json 
import numpy as np
import pickle
from tensorflow import keras
owner = None #your ID
channel = None #your channel
bot = commands.Bot(command_prefix="!")
class AIinfo:
    username = "User"
with open("intents.json") as file:
    data = json.load(file)
model = keras.models.load_model('chat_model')
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
with open('label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)
max_len = 20
@bot.event
async def on_message(message: discord.Message):
    if message.channel.id == channel:
        inp = message.content
        print(f"{message.author}: {inp}")
        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                             truncating='post', maxlen=max_len))
        tag = lbl_encoder.inverse_transform([np.argmax(result)])
        for i in data['intents']:
            if i['tag'] == tag:
                resp = np.random.choice(i['responses'])
                respp = random.choice(i['responses'])
                #print(Fore.LIGHTMAGENTA_EX + "Pink:" + Style.RESET_ALL , resp)
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
                        respp = respp+f" {message.author.display_name}"
                if message.author.id == bot.user.id:
                    pass
                else:
                    if message.author.id == owner:
                        if message.content.lower() == "quit":
                            await message.channel.send("Shutting down PinkAI..")
                            quit()
                        else:
                            await message.channel.send(respp)
                    else:
                        await message.channel.send(respp)

@bot.event
async def on_ready():
    print("Bot is ready")
    await bot.get_channel(channel).send("PinkAI Online")

bot.run("token")
