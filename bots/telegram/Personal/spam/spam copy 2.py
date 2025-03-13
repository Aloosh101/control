from telethon import TelegramClient
from time import sleep
import telethon
import asyncio

client = TelegramClient("session_name2", api_id="1234567", api_hash="123456kjh")


def save_count(count):
    with open ("count2.txt", "w") as f:
        f.write (str(count))


def load_count():
    try:
        with open ("count2.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0


async def send_message(users: list,message: str):
    
    await client.connect()
    
    if not await client.is_user_authorized():
        phone = "+37121428637"
        await client.send_code_request(phone, force_sms=False)
        value = input("Enter login code: ")
        try:
            me = await client.sign_in(phone, code=value)
        except telethon.errors.SessionPasswordNeededError:
            password = input("pass: ")
            me = await client.sign_in(password=password)
    
    for x in range(len(users)):
        await client.send_message(users[x], message)
        if (x+1) == len(users):
            break
    await client.disconnect()

    
    print('Message sent successfully')



count = load_count()
loop = asyncio.get_event_loop()
while True:
 
    task = loop.create_task(send_message(["https://t.me/FF_FFF",'https://t.me/Paris200k','https://t.me/K999kk9'],"متوفر نشر تلقائي\n"+
    "2000 رسالة ب100 نقطة\n"+
    "4000 رسالة ب200 نقطة\n"+
    "6000 رسالة ب300 نقطة\n"+
    "8000 رسالة ب400 نقطة\n"+
    "10000 رسالة ب500 نقطة\n"+
    "--------------------------\n"+
    "برمجة بوتات تليثون - تليكرام من الصفر\n"+
    "برمجة مواقع - بوتات دسكورد - برامج اخرى على حسب الطلب❗️⚠️\n"+
    "لترد عليه راسلني خاص @mr_code_101"))
    count += 1
    save_count(count)
    
    loop.run_until_complete(asyncio.sleep(100))