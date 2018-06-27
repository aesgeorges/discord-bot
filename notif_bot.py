from twitch import TwitchClient
import discord
import asyncio
import json
import os

CLIENT_ID = os.environ.get('CLIENT_ID')
PLAYER_ID = [os.environ.get('FRVMED_ID'), os.environ.get('FEROCT_ID')]
TOKEN = os.environ.get('TOKEN')

#192336272 framed
#55039613 Arms dude
#26490481 Fortnite dude

# DISCORD
discordClient = discord.Client()

# TWITCH
client = TwitchClient(client_id=CLIENT_ID)

# checking stream
def stream(streamer):
    channel = client.channels.get_by_id(streamer)
    streamStatus = client.streams.get_stream_by_user(streamer)
    print (streamStatus)
    if streamStatus is not None:
        notif = channel.display_name
        return notif
    else:
        return

@discordClient.event
async def on_ready():
    print('Logged in as')
    print(discordClient.user.name)
    print(discordClient.user.id)
    print('--------')

@discordClient.event
async def on_message(message):
    if message.author == discordClient.user:
        return
    if message.content.startswith('!hello'):
        msg = 'Wasup hot boi {0.author.mention}'.format(message)
        print ('command !hello prompted')
        await discordClient.send_message(message.channel, msg)
    if message.content.startswith('!bye'):
        msg = 'See ya! {0.author.mention}'.format(message)
        print ('commande !bye prompted')
        await discordClient.send_message(message.channel, msg)

async def stream_check():
    await discordClient.wait_until_ready()
    streaming = False
    while not discordClient.is_closed:
        for streamer in PLAYER_ID:
            print(streamer)
            print ('checking stream...')
            stream(streamer)
            status = stream(streamer)
            print (status)
            if streaming == False:
                if status is not None:
                    channel = client.channels.get_by_id(streamer)
                    this = client.streams.get_stream_by_user(streamer)
                    game = this.game
                    url = channel.url
                    msg = channel.display_name + ' is streaming ' + game + '. Join him! \n' + url
                    streaming = True
                    print ('client started stream')
                    await discordClient.send_message(discordClient.get_channel('405195595955961863'), msg)
                else:
                    print ('not streaming')
            if streaming == True:
                if status is None:
                    channel = client.channels.get_by_id(streamer)
#                    msg = channel.display_name + ' stopped streaming, see ya next time.'
                    streaming = False
                    print ('client stopped stream.')
                    await discordClient.send_message(discordClient.get_channel('405195595955961863'), msg)
            await asyncio.sleep(5)

discordClient.loop.create_task(stream_check())
discordClient.run(TOKEN)
