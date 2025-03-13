import discord
from discord.ext import commands
import requests
import os

intents = discord.Intents.default() 
client = commands.Bot(command_prefix = '', intents=intents)
@client.event
async def on_ready():
    print('Bot is ready.')


@client.command()
async def chat(ctx, *, message):
    print(message)
    url = "https://www.bing.com/chat"
    payload = {"message": message}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    reply = data["reply"]
    await ctx.send(f'Bing chat says: {reply}')




@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        commandList = []
        for command in client.commands:
            commandList.append(command.name)
        print(commandList)
        await ctx.send("الامر غير موجود.")

client.run(os.environ['TOKEN_DISCORD'] )
