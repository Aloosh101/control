import os
import asyncio
import discord
import config
from datetime import datetime, timedelta

client = discord.Client(intents=discord.Intents.all())
SERVER_ID = config.SERVER_ID


@client.event
async def on_ready():
  print('Logged in as')
  print(client.user.name)
  print(client.user.id)
  
  server = client.get_guild(SERVER_ID)
  print(f'Monitoring {server.name}')
  print('------')

start_times = {}

@client.event
async def on_presence_update(before, after):
  if after.guild.id == SERVER_ID:

    if after.bot:
        return
      
    
    for activity in after.activities:
      
      if activity.type == discord.ActivityType.playing and not before.activities:
        current_time = datetime.now().strftime('%d/%m/%Y %H:%M')

        play_time = datetime.now()
        
        start_times[after.id] = play_time
        
        channel = client.get_channel(config.gameChannelID)
        
        await channel.send(
          f'**{after.name}** started playing **"{activity.name}"** at **"{current_time}"**! (ID: {after.id})'
        )

    
    for activity in before.activities:
      
      if before.activity is not None and before.activity.type == discord.ActivityType.playing and before.id in start_times and after.activity is None:
        current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
    
        
        play_time = datetime.now()
        if before.id in start_times:
          
          start_time = start_times[before.id]          
          
          total_playtime = play_time - start_time
          
          total_seconds = total_playtime.total_seconds()
          days, remainder = divmod(total_seconds, 86400)
          hours, remainder = divmod(remainder, 3600)
          minutes, seconds = divmod(remainder, 60)
      
          
          formatted_playtime = f'{int(days)} days, {int(hours):02}:{int(minutes):02}:{int(seconds):02}'
          start_times.pop(before.id)
        else:
           
          formatted_playtime = "UNKOWN"
        
        channel = client.get_channel(config.gameChannelID)
        
        await channel.send(
            f'**{before.name}** stopped playing **"{activity.name}"** at **"{current_time}"** after playing for **"{formatted_playtime}"**! (ID: {before.id})'
        )
    
    if before.status != discord.Status.online and after.status == discord.Status.online:
      
      channel = client.get_channel(config.statusChannelID)
      print('Status Event triggered')
      if channel is not None:
        await channel.send(f'{after.name} just went online! (ID: {after.id})')

client.run(config.TOKEN)
