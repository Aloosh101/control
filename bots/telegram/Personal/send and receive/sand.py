

from telethon import TelegramClient
import asyncio
import telethon

api_id = 25811123
api_hash = '0af132b0bb94baba46ae611a56dffd7f'


client = TelegramClient('session_name', api_id, api_hash)

client.start()


async def send_message(message: str,username: str):
    if message.startswith("f="):
        
        file = message[2:]
        caption = input("Enter your caption or skip: ")
        
        if caption:
            await client.send_file(username,file,caption=caption)
            
            print("File sent!")

        else:
            await client.send_file(username,file)
            
            print("File sent!")
    else:   
        
        await client.send_message(username, message)
        
        print("Message sent!")

loop = client.loop
username = input("Enter the username: ")
while True:
    message = input("Enter your message: ")
    
    loop.run_until_complete(asyncio.gather(
        send_message(str(message),username)
    ))
