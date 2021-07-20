import logging
import os
import asyncio
import discord  # pylint: disable=import-error
from dotenv import load_dotenv  # pylint: disable=import-error
from discord.ext import commands

#Implements logging into application
logging.basicConfig(level=logging.INFO) #NOTE:bot takes more time to start up, disable for speedier startups

#Gather private info from env
load_dotenv()
token = os.getenv('Discord_Token')
server = os.getenv('Server_Name')

#A client interacts with the Discord API
client = discord.Client()

inprogress = 0 #basic / temporary solution for a check

@client.event
async def on_ready(): #Activates once connection to Discord is established
    # for guild in client.guilds: #Iterates through all of the servers that the bot is connected to
    #     if guild.name == server:
    #         break #Leave as soon as server id is found
    
    #Print out name of bot and the server its on
    print('Logging in as  {0.user}'.format(client))

@client.event
async def on_message(message): #upon hearing the call of ~
    if str(message.channel) == "bot-speak-🤖": #the bot will only respond to commands made in the appropriate channel  
        if message.author == client.user: #prevents recursion with self
            return
        if message.content.startswith('~hello'):
            await message.channel.send('Hello {}.'.format(message.author.name)) #the format command fills in the {} with whatever is in the ()
        elif message.content.startswith('~announce'):
            global inprogress
            if inprogress == 0: #crude method to prevent multiple instances of the command being used
                inprogress = 1
                try:
                    msg = await message.author.send('Please respond with the phrase you would like me to announce in **{}**:'.format(message.guild.name)) #message is sent directly to author rather than in the guild
                except discord.Forbidden: #failsafe in-case of error
                    await message.author.send('Error')
                    inprogress = 0
                    return

                def check(author):
                    def check2(message):
                        if message.author != author or message.channel != msg.channel: #checks that the message is created by the author and that it is done via direct message only
                            return False
                        else:
                            return True
                    return check2

                try:
                    msg2 = await client.wait_for('message', check=check(message.author), timeout=30) #bot waits for a response from the author via direct message for 30 seconds
                except asyncio.TimeoutError: #if the author has failed to reply to the bot within 30 seconds
                    await message.author.send('You took too long!')
                    inprogress = 0
                    return
                channel1 = client.get_channel(708494762377740369) #direct the bot to message in the appropriate channel
                await channel1.send('@everyone')
                await channel1.send('```{} wants to announce:\n{}```'.format(message.author.name, msg2.content)) #{} are variable placeholders, variables inserted via .format
                inprogress = 0
                
            else:
                await message.author.send('Someone is currently using trying to post an announcement, please wait!')
        elif (message.content.startswith('~quit')):
            await client.logout()
        else:
            await message.channel.send('I do not know that one.')

client.run(token)
