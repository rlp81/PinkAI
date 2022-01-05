import discord
from discord.ext import commands
import random
import json 
import numpy as np
import pickle
from tensorflow import keras
startchannel = None #your channel
owner = None #your user id
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

@bot.command(name="quit")
async def quit(context):
    if context.author.id == owner:
        quit()

@bot.command(name="info")
async def info(context):
    emb = discord.Embed(title="PinkAI info",description=f"All code for the bot can be found in the [github](https://github.com/rlp81/PinkAI)\nI was created by rlp81 (Coal#3591) for a friend named Pink hense the name.")
    await context.send(embed=emb)

@bot.command(name="setaichannel",aliases=["aichannel"])
async def aichannel(context, channel: discord.TextChannel = None):
    if channel != None:
        with open("info.json","r") as f:
            info = json.load(f)
        info[channel.guild.id] = channel.id
        with open("info.json","w") as f:
            info = json.dump(info,f,indent=4)
        await context.send(f"Set PinkAI to {channel}!")
    else:
        await context.send("Mention a channel to set PinkAI to!")

@bot.command(name="request-logs", aliases=["rl","requestlogs","reqlogs","reqlog"])
async def requestlogs(context):
    await context.author.send(file=discord.File("log.txt"))
    await context.send("Sent you AI logs!")

@bot.event
async def on_message(message: discord.Message):
    channel = None
    with open("info.json","r") as f:
        info = json.load(f)
    if str(message.guild.id) in info:
        channel = info[str(message.guild.id)]
        if channel == message.channel.id:
            inp = message.content
            print(f"{message.author.display_name}: {inp}")
            with open("log.txt", "a") as file:
                file.write(f"{message.author.display_name}: {inp}\n")
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
        else:
            pass
    await bot.process_commands(message)
@bot.event
async def on_ready():
    print("Bot is ready")
    await bot.get_channel(startchannel).send("PinkAI Online")

bot.run("token")
