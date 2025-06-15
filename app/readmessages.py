import discord
import json
import os
#import vibetoys
#import asyncio
import subprocess
import random
#import vibe_prom_toys as vp
import winsdk.windows.devices.bluetooth.advertisement as wwda
import winsdk.windows.storage.streams as wwss
import asyncio
import time
import threading
import asyncio
import logging
import sys
import json
import asyncio
import websockets
#from dotenv import load_dotenv

buttplug_server_is_running = False
def test_url(url, data=""):
    async def inner():
        async with websockets.connect(url) as websocket:
            await websocket.send(data)
    return asyncio.get_event_loop().run_until_complete(inner())

print("testing if buttplug server is running...")
try:
    test_url("ws://127.0.0.1:12345/")
    buttplug_server_is_running = True
except:
    buttplug_server_is_running = False
    print("buttplug server not reached, turning off integrations...")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents = intents)
guild = discord.Guild
messages =  []

bot_name = "testme#9594"

rootpath = os.path.dirname(__file__)
fullpath_helper = ""
with open(rootpath + '\\..\\vendor\\BP.IO.CMD.exe', 'r') as file:
    fullpath_helper = os.path.realpath(file.name)
print("found full path of helper program as ", fullpath_helper)

bot_clip_cycles = 0

emoji_list = [":smile:", ":grin:", ":blush:", ":disguised_face:", ":zany_face:", ":smiling_imp:"]
def get_rand_emoji():
    return random.choice(emoji_list)

def get_triggers():
    import json

    data = {}
    
    with open(rootpath + '\\..\\config\\action_triggers.json', 'r') as file:
        data = json.load(file)

    return data

async def to_act_or_not_to_act(message, triggers):
    global bot_clip_cycles
    for keyword in triggers:
        if( message.content.find(keyword) > -1 ):
            action_text = triggers[keyword]
            action_params = action_text.split()
            device_index = action_params[0].split("=")[1]
            strength = action_params[1].split("=")[1]
            duration = action_params[2].split("=")[1]
            channel = client.get_channel(int(1383417107764613211)) # find the channel with the channel ID
            
            if( len(action_params) > 3 ):
                bot_response = action_params[3].split("=")[1]
                print(message.author.name)
                if( bot_response == "1" and message.author.name != "testme" ):
                    #bot_clip_cycles += 1
                    bot_response = "I am a good bot! "+get_rand_emoji()+" :heart: Thank you for saying so, here have some vibes"
                if( bot_response == "2" and message.author.name != bot_name):
                    bot_response = "Hey you take that back I'm nice! :angry: I'll vibe you!"
                await channel.send(bot_response)
            else:
                await channel.send("Hai! "+get_rand_emoji()+" I received a command for vibing! Turning all the toys on for "+str(duration)+" seconds at "+str(strength)+"%... Enjoy :smiling_imp:")

            print("have index, duration, str as ", device_index, duration, strength)

            prom_str = int((int(strength)/100)*3)
            print("have prom str ", prom_str)
            
            #import os
            #os.system(fullpath_helper + " " + strength + " " + duration)
            #os.spawnl(os.P_DETACH, fullpath_helper, strength, duration)
            await SHAKE(prom_str, int(duration))

            print("have action params as ", action_params)

            # the buttplug action helper will block for the requested duration, which will also block this thread
            if( buttplug_server_is_running == True ):
                subprocess.run([fullpath_helper, strength, duration])
            # if the buttplug server is not running, we can avoid running the other program and just sleep to block manually
            else:
                time.sleep(int(duration))
            
            await STOP()
            #t1.start()
            #t2.start()

            #await client.send_message(client.get_channel("1383417107764613211"), 'hello world!')
            

advt_pub = None

async def send_command(command,duration):
    global advt_pub
    advt_publish = wwda.BluetoothLEAdvertisementPublisher()
    advt_pub = advt_publish
    print("have advt pub stat as ", advt_publish.status)# value = 1 for started I guess
    print("have advt pub as ", str(advt_publish.status))
    manufacturerData  = wwda.BluetoothLEManufacturerData()
    manufacturerData.company_id = 0xFF
    writer = wwss.DataWriter()
    writer.write_bytes(bytearray.fromhex("0000006db643ce97fe427c"+command))
    manufacturerData.data =  writer.detach_buffer()
    advt_publish.advertisement.manufacturer_data.append(manufacturerData)
    advt_publish.start()
    #time.sleep(duration)
    print("have advt pub stat as ", str(advt_publish.status))
    #while(str(advt_publish.status) != "2"):
    #    pass
    #advt_publish.stop()


async def STOP():
    advt_pub.stop()


async def SHAKE(mode,duration):
    if(mode==0):
        await send_command("C5175C",duration)
    elif(mode==1):
        await send_command("F41D7C",duration)
    elif(mode==2):
        await send_command("F7864E",duration)
    elif(mode==3):
        await send_command("F60F5F",duration)
    elif(mode==4):
        await send_command("F1B02B",duration)
    elif(mode==5):
        await send_command("F0393A",duration)
    elif(mode==6):
        await send_command("F3A208",duration)
    elif(mode==7):
        await send_command("F22B19",duration)
    elif(mode==8):
        await send_command("FDDCE1",duration)
    elif(mode==9):
        await send_command("FC55F0",duration)



async def OFF():
    asyncio.run(send_command("E5157D",0.001))



print("Bot started")
@client.event
async def on_message(message):
    
    channelIDsToListen = [ 1383417107764613211 ] # put the channels that you want to listen to here
    print("have message " + str(message.content) + " on channel " + str(message.channel.id))
    
    if message.channel.id in channelIDsToListen:

        if message.content != "" and message.author.name.find(bot_name) == -1:
            print(dir(message))
            print(message.author)
            messages.append(message)

        await to_act_or_not_to_act(message, get_triggers())

print("using env file at ", rootpath + "\\.env")
def get_env_data_as_dict(path: str) -> dict:                             
    with open(path, 'r') as f: 
        return dict(tuple(line.replace('\n', '').split('=')) for line in f.readlines() if not line.startswith('#'))

vars_dict = get_env_data_as_dict(rootpath + "\\.env")
os.environ.update(vars_dict)
DOTNET_SECRET = os.getenv('DISCORD_SECRET')
print("have dotnet secret as ", DOTNET_SECRET)
client.run(DOTNET_SECRET)