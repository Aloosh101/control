
from telethon import TelegramClient, events
import telethon
from telethon.utils import get_input_media


api_id = 123456789
api_hash = '12345678'


client = TelegramClient('session_name1', api_id, api_hash)

client.start()


async def handle_new_message(event):
    
    print("Received:", event.message.text)

    
    if event.message.media:
        
        path = await client.download_media(event.message.media, file="./downloads")
        
        print("Media saved to", path)


client.add_event_handler(handle_new_message, events.NewMessage(from_users='mr_code_101'))


client.run_until_disconnected()


