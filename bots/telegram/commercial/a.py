
from telethon import TelegramClient, events
import asyncio
from time import sleep
from telethon.utils import get_input_media


api_id = 123456789
api_hash = '123456uil,'


client = TelegramClient('session_name', api_id, api_hash)

async def get_last_message(chat):
    
    await client.start()
    a = await client.get_me()
    print(a.phone)
    sleep(20)
    message = await client.get_messages(chat, limit=1)
    
    print(message[0].text)
    
    await client.stop()
    exit(1)


asyncio.get_event_loop().run_until_complete(get_last_message(777000))
