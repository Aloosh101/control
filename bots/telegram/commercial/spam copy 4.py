from telethon.sync import TelegramClient, events

client = TelegramClient ('session_name2',api_id=25811123, api_hash="0af132b0bb94baba46ae611a56dffd7f")

groups = {}

async def get_last_msg(event):
    
    user = await event.get_sender()
    
    last_msg = await client.get_messages(user, limit=1)
    
    return last_msg[0].id


@client.on(events.NewMessage())
async def handler(event):
    
    min_id = await get_last_msg(event)
    
    if event.id >= min_id:
        if event.is_reply: 
            print("run")
            await event.reply("اني مجرد بوت نشر تلقائي خاص للعروض الخاصة بي") 
        if event.is_private: 
            print("run private")
            await event.reply("انا مجرد حساب نشر تلقائي عروضي:\n"+
            "متوفر نشر تلقائي\n"+
            "2000 رسالة ب100 نقطة\n"+
            "4000 رسالة ب200 نقطة\n"+
            "6000 رسالة ب300 نقطة\n"+
            "8000 رسالة ب400 نقطة\n"+
            "10000 رسالة ب500 نقطة\n"+
            "--------------------------\n"+
            "برمجة بوتات تليثون - تليكرام من الصفر\n"+
            "برمجة مواقع - بوتات دسكورد - برامج اخرى على حسب الطلب❗️⚠️\n"+
            "لترد عليه راسلني خاص @mr_code_101")
        
        else:
            
            chat_username = event.chat.username
            
            if chat_username not in groups:
                groups[chat_username] = event.chat_id
client.start() 
client.run_until_disconnected() 
