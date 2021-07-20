import discord
import asyncio
from discord.ext import commands

client = discord.Client()
id = client.get_guild('server_id')

inprog = 0
counter = 0
valid_channels = ['commands']

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message): #This event occurs everytime a message is sent in the guild
    if str(message.channel) == "commands":

        if message.content.startswith('$greetings'): #Command and automated response
            await message.channel.send('Hello {}!'.format(message.author.name))

        #Organize process by making it so that the message must be sent to the bot via a direct message
        #Only the original author of the command message may respond to the promp

        if message.content.startswith('$repeat'):
            global announce
            if announce == 0:
                announce = 1
                try:
                    msg = await message.author.send('Please respond with the phrase you would like me to repeat in **{}**:'.format(message.guild.name)) #Sends a direct message to the author of the command
                except discord.Forbidden: #In case of error
                    await message.author.send('Error')
                    announce = 0
                    return

                def check(author):
                    def check2(message):
                        if message.author != author or message.channel != msg.channel:
                            return False
                        else:
                            return True
                    return check2

                try:
                    msg2 = await client.wait_for('message', check=check(message.author), timeout=30) #bot waits for a response from the author via direct message
                except asyncio.TimeoutError:
                    await message.author.send('You took too long!')
                    announce = 0
                    return
                general = client.get_channel(712435402601922914)
                await general.send('@everyone')
                await general.send('```{} wants to announce:\n{}```'.format(message.author.name, msg2.content)) #posts the message in the chat
                announce = 0
                
            else:
                await message.author.send('Someone is currently using the repeat command, please wait!')

        if message.content.startswith('$startpoll'):
            global question
            if question == 0:
                question = 1
                try:
                    msg = await message.author.send('Please respond here with the specific question you would like to ask in **{}**:'.format(message.guild.name)) #Sends a direct message to the author of the command
                except discord.Forbidden: #In case of error
                    await message.author.send('Error')
                    question = 0
                    return

                def check(author):
                    def check2(message):
                        if message.author != author or message.channel != msg.channel:
                            return False
                        else:
                            return True
                    return check2

                try:
                    msg2 = await client.wait_for('message', check=check(message.author), timeout=30) #bot waits for a response from the author via direct message
                except asyncio.TimeoutError:
                    await message.author.send('You took too long!')
                    question = 0
                    return

                try:
                    msg = await message.author.send('What is the first option to your question?')
                except discord.Forbidden:
                    await message.author.send('Error')
                    question = 0
                    return
                
                try:
                    msg3 = await client.wait_for('message', check=check(message.author), timeout=30)
                except asyncio.TimeoutError:
                    await message.author.send('You took too long!')
                    question = 0
                    return

                try:
                    msg = await message.author.send('What is the second option to your question?')
                except discord.Forbidden:
                    await message.author.send('Error')
                    question = 0
                    return
                
                try:
                    msg4 = await client.wait_for('message', check=check(message.author), timeout=30)
                except asyncio.TimeoutError:
                    await message.author.send('You took too long!')
                    question = 0
                    return
                
                general = client.get_channel(712435402601922914)
                await general.send('@everyone')
                await general.send('```{} has created a poll:\n{}```'.format(message.author.name, msg2.content)) #posts the message in the chat
                await general.send('```Option 1: {}```'.format(msg3.content))
                await general.send('```Option 2: {}```'.format(msg4.content))
                await general.send('```Please respond with $vote1 or $vote2```')
            else:
                await message.author.send('Someone is currently trying to create a poll, please wait!')

        if message.content.startswith('$endpoll'):
            if question == 0:
                message.channel.send('There is no poll currently!')
            else:
                question = 0

        if message.content.startswith('$vote1'):
            global op1
            op1 = op1 + 1
            await message.channel.send('```Your vote has been recorded, {}```'.format(message.author.name))

        if message.content.startswith('$vote2'):
            global op2
            op2 = op2 + 1
            await message.channel.send('```Your vote has been recorded, {}```'.format(message.author.name))
        
        if message.content.startswith('$polldisplay'):
            await message.channel.send('```Option 1: {} --- Option 2: {}```'.format(op1, op2))

        if message.content.startswith("$pollreset"):
            op1 = 0
            op2 = 0
            await message.channel.send('```The votes have been reset.```')

        if message.content.startswith("$off"):
            await client.logout()
client.run('token')