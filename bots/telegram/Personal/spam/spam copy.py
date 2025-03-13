from telethon import TelegramClient
from time import sleep
import telethon
import asyncio

client = TelegramClient("session_name", api_id="123456789", api_hash="234567ijy65")


def save_count(count):
    with open ("count.txt", "w") as f:
        f.write (str(count))


def load_count():
    try:
        with open ("count.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0


async def send_message(users: list,message: str):
    
    await client.connect()
    
    if not await client.is_user_authorized():
        phone = "+964 7860653754"
        await client.send_code_request(phone, force_sms=False)
        value = input("Enter login code: ")
        try:
            me = await client.sign_in(phone, code=value)
        except telethon.errors.SessionPasswordNeededError:
            password = ("Narmin1Ali")
            me = await client.sign_in(password=password)
    
    for x in range(len(users)):
        await client.send_message(users[x], message)
        if (x+1) == len(users):
            break
    sleep(10)
    for x in range(len(users)):
        await client.send_message(users[x], "حساب انستقرام 15.8k \nللبيع السعر 5اسيا\nربط رقم يتحول ب رقمك \nتواصل @ZARO_MY_BOT")
        if (x+1) == len(users):
            break
    await client.disconnect()

    
    print('Message sent successfully')


loop = asyncio.get_event_loop()

count = load_count()
while True:
    
    task = loop.create_task(send_message(["t.me/zzzzzsTaR"],"مطلوب ارقام لاتيفي كميه ب 500\n"+
"نقاط العرب\n\n"+
"رد علي بلخاص: @HAhahshse"))    
    count += 1
    save_count (count)
    
    loop.run_until_complete(asyncio.sleep(19))
    
    if count >= 2000:
        loop.stop ()
        break

