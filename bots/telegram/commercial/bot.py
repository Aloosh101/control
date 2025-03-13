

import telebot
import sqlite3
import logging
from telethon.sync import TelegramClient
from time import sleep
from telebot import types
from telethon.tl.functions.messages import StartBotRequest
import re


TOKEN = "6161054321:AAFTRINCSsYCTyMe8SZHBbkIcQsVnJKdWpc"


bot = telebot.TeleBot(TOKEN)


client = TelegramClient("bot", api_id="25153583", api_hash="35543407ec1e319a3927f267183adb5d")


user_data = {}


def validate_message(message):
    
    assert message.text != "", "الرسالة فارغة"
    
    assert len(message.text) <= 1000, "الرسالة طويلة جدا"
    
    assert not any([message.entities, message.caption_entities, message.audio, message.document, message.photo, message.sticker, message.video, message.voice]), "الرسالة تحتوي على عناصر غير مسموح بها"


def validate_users(users):
    
    assert users != [], "القائمة فارغة"
    
    assert len(users) == len(set(users)), "القائمة تحتوي على عناصر مكررة"
    
    assert len(users) <= 10, "القائمة تحتوي على أكثر من 10 عناصر"


def validate_link(link):
    
    assert isinstance(link, str), "الرابط ليس سلسلة نصية"
    
    assert link.startswith("https://t.me/zmmbot?start="), "الرابط غير صحيح"


def reset_user_data(user_id):
    user_data[user_id] = {"points": None, "message": None, "users": None}


def check_the_link(link: str, required_points: int):
    
    client.start()
    params = link.split('=')[-1] 
    request = StartBotRequest('zmmbot', 'zmmbot', params) 
    try:
        result = client(request) 
        sleep(0.5)
        message = client.get_messages('zmmbot')[0] 
        pattern = r'\d+' 
        matches = re.findall(pattern, message.text) 
        number = matches[0] 
        if int(number) == required_points:
            return [1]
        elif int(number) > required_points:
            client.send_message("https://t.me/zmmbot","/start")
            sleep(0.5)
            message = client.get_messages('zmmbot')[0] 
            message.click(text='تحويل نقاط')
            number = str(int(number) - required_points)
            client.send_message("https://t.me/zmmbot",number)
            sleep(0.5)
            points_message = client.get_messages('zmmbot')[0] 
            return [2,points_message.text]
        elif int(number) < required_points:
            client.send_message("https://t.me/zmmbot","/start")
            sleep(0.5)
            message = client.get_messages('zmmbot')[0] 
            message.click(text='تحويل نقاط')
            client.send_message("https://t.me/zmmbot",str(number))
            sleep(0.5)
            points_message = client.get_messages('zmmbot')[0] 
            return [3,points_message.text]
    except IndexError:
        return [4]
    except Exception as e:
        logging.error(e) 
        return ("لقد حصل خطا ما\nراسل المبرمج ان تكررت المشكلة لحلها باقرب وقت\n المبرمج: @mr_code_101")
    finally:
        
        client.disconnect()


def add_list(users, message, times):
    con = sqlite3.connect("tutorial.db")
    
    cur = con.cursor()
    
    users_str = ",".join(users)
    cur.execute("INSERT INTO list (users, message, times, sent) VALUES (?, ?, ?, 0)", (users_str, message, times))
    con.commit()
    con.close()


def update_list(list_id, users, message, times):
    con = sqlite3.connect("tutorial.db")
    
    cur = con.cursor()
    
    users_str = ",".join(users)
    cur.execute("UPDATE list SET users = ?, message = ?, times = ? WHERE id = ?", (users_str, message, times, list_id))
    con.commit()
    con.close()


def send_message_to_users(user_id):
    
    data = user_data[user_id]
    
    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()
    
    cur.execute("SELECT * FROM list WHERE message = ? AND users = ? AND times = ?", 
                (data["message"], ",".join(data["users"]), data["points"] // 100 * 2000))
    row = cur.fetchone()
    
    if row is None:
        add_list(data["users"], data["message"], data["points"] // 100 * 2000)
        
        list_id = cur.lastrowid
    
    else:
        list_id = row[0]
        sent_times = row[4]
    
    con.close()
    
    client.start()
    
    users = data["users"]
    
    message_text = data["message"]
    
    points = data["points"]
    
    times = points // 100 * 2000
    
    if row is None or sent_times == 0:
        
        bot.send_message(user_id, f"سيتم إرسال رسالتك {times} مرة إلى {len(users)} مستخدم.")
        
        for i in range(times):
            
            for user in users:
                try:
                    client.send_message(user, message_text) 
                except Exception as e:
                    logging.error(e) 
            sleep(1) 
        
        client.disconnect()
        
        con = sqlite3.connect("tutorial.db")
        cur = con.cursor()
        
        cur.execute("UPDATE list SET sent = ? WHERE id = ?", (times, list_id))
        con.commit()
        con.close()
        
        bot.send_message(user_id, "تم إرسال رسالتك بنجاح.")
    
    elif sent_times < times:
        
        bot.send_message(user_id, f"سيتم إعادة إرسال رسالتك {times - sent_times} مرة إلى {len(users)} مستخدم.")
        
        for i in range(times - sent_times):
            
            for user in users:
                try:
                    client.send_message(user, message_text) 
                except Exception as e:
                    logging.error(e) 
            sleep(1) 
        
        client.disconnect()
        
        con = sqlite3.connect("tutorial.db")
        cur = con.cursor()
        
        cur.execute("UPDATE list SET sent = ? WHERE id = ?", (times, list_id))
        con.commit()
        con.close()
        
        bot.send_message(user_id, "تم إعادة إرسال رسالتك بنجاح.")
    
    elif sent_times == times:
        
        client.disconnect()
        
        bot.send_message(user_id, "لا يمكن إعادة إرسال رسالتك لأنك قد استنفذت عدد المرات المطلوبة.")
    
    del user_data[user_id]


@bot.message_handler(commands=["start", "help"])
def handle_start_help(message):
    
    user_id = message.from_user.id
    
    if user_id not in user_data:
        
        user_data[user_id] = {}
        user_data[user_id]["users"] = []
        user_data[user_id]["message"] = ""
        user_data[user_id]["link"] = ""
        user_data[user_id]["points"] = 0
    
    bot.send_message(user_id, "مرحبا بك في بوت التجارة. هذا البوت يسمح لك بإرسال رسائل إلى قائمة من المستخدمين المستهدفين مقابل عدد معين من النقاط. النقاط يمكن الحصول عليها من خلال رابط خاص يتم تفعيله عن طريق بوت آخر يسمى zmmbot. لإرسال رسالة، يجب أن تتبع الخطوات التالية:\n1- أضف قائمة جديدة من المستخدمين المستهدفين أو تعديل قائمة موجودة.\n2- أضف نص الرسالة التي تريد إرسالها.\n3- أضف رابط صحيح يحتوي على عدد كافي من النقاط.\n4- اضغط على زر إرسال الرسالة.")
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("إضافة قائمة جديدة", callback_data="add_new_list"))
    markup.add(types.InlineKeyboardButton("تعديل قائمة موجودة", callback_data="edit_existing_list"))
    
    bot.send_message(user_id, "اختر ما تريد فعله.", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    
    user_id = call.from_user.id
    
    data = user_data[user_id]
    
    if call.data == "add_new_list":
        
        bot.send_message(user_id, "أدخل قائمة المستخدمين المستهدفين بالشكل التالي:\n@user1\n@user2\n@user3\n...")
        
        bot.register_next_step_handler(call.message, handle_users)
    
    elif call.data == "edit_existing_list":
        
        bot.send_message(user_id, "أدخل معرف القائمة التي تريد تعديلها.")
        
        bot.register_next_step_handler(call.message, handle_list_id)
    
    elif call.data == "add_message":
        
        bot.send_message(user_id, "أدخل نص الرسالة التي تريد إرسالها.")
        
        bot.register_next_step_handler(call.message, handle_message)
    
    elif call.data == "add_link":
        
        bot.send_message(user_id, "أدخل رابط صحيح.")
        
        bot.register_next_step_handler(call.message, handle_link)


def handle_users(message):
    
    user_id = message.from_user.id
    try:
        
        validate_message(message)
        
        users = message.text.strip().split()
        
        validate_users(users)
        
        user_data[user_id]["users"] = users
        
        bot.send_message(user_id, "تم حفظ قائمة المستخدمين بنجاح.")
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("إضافة رسالة", callback_data="add_message"))
        markup.add(types.InlineKeyboardButton("إضافة رابط", callback_data="add_link"))
        markup.add(types.InlineKeyboardButton("تعديل قائمة موجودة", callback_data="edit_existing_list"))
        
        bot.send_message(user_id, "اختر ما تريد فعله.", reply_markup=markup)
    except AssertionError as e:
        
        bot.send_message(user_id, e.args[0])
        bot.send_message(user_id, "أعد إدخال قائمة المستخدمين بالشكل التالي:\n@user1\n@user2\n@user3\n...")
        bot.register_next_step_handler(message, handle_users)


def handle_list_id(message):
    
    user_id = message.from_user.id
    try:
        
        validate_message(message)
        
        list_id = int(message.text.strip())
        
        con = sqlite3.connect("tutorial.db")
        cur = con.cursor()
        
        cur.execute("SELECT * FROM list WHERE id = ?", (list_id,))
        row = cur.fetchone()
        
        con.close()
        
        if row is None:
            
            bot.send_message(user_id, "لا يوجد قائمة بهذا المعرف. أدخل معرف صحيح.")
            bot.register_next_step_handler(message, handle_list_id)
        else:
            
            users = row[1].split(",") 
            message_text = row[2]
            times = row[3]
            sent_times = row[4]
            
            user_data[user_id]["users"] = users
            user_data[user_id]["message"] = message_text
            user_data[user_id]["points"] = times // 2000 * 100
            
            bot.send_message(user_id, f"هذه هي بيانات القائمة التي اختارتها:\nالمستخدمون: {', '.join(users)}\nالرسالة: {message_text}\nالأوقات: {times}\nالأوقات المرسلة: {sent_times}")
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("تعديل قائمة المستخدمين", callback_data="edit_users"))
            markup.add(types.InlineKeyboardButton("تعديل نص الرسالة", callback_data="edit_message"))
            markup.add(types.InlineKeyboardButton("تعديل عدد الأوقات", callback_data="edit_times"))
            markup.add(types.InlineKeyboardButton("إرسال الرسالة", callback_data="send_message"))
            
            bot.send_message(user_id, "اختر ما تريد فعله.", reply_markup=markup)
    except AssertionError as e:
        
        bot.send_message(user_id, e.args[0])
        bot.send_message(user_id, "أعد إدخال معرف صحيح.")
        bot.register_next_step_handler(message, handle_list_id)

          

def handle_message(message):
    
    user_id = message.from_user.id
    
    validate_message(message)
    
    message_text = message.text
    
    user_data[user_id]["message"] = message_text
    
    bot.send_message(user_id, "تم حفظ نص الرسالة بنجاح.")
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("إضافة قائمة جديدة", callback_data="add_new_list"))
    markup.add(types.InlineKeyboardButton("إضافة رابط", callback_data="add_link"))
    markup.add(types.InlineKeyboardButton("تعديل قائمة موجودة", callback_data="edit_existing_list"))
    
    bot.send_message(user_id, "اختر ما تريد فعله.", reply_markup=markup)

def handle_link(message):
    
    user_id = message.from_user.id
    try:
        
        validate_message(message)
        
        link = message.text.strip()
        
        validate_link(link)
        
        user_data[user_id]["link"] = link
        
        status = check_the_link(link, 100)
        
        if status[0] == 1:
            
            
            bot.send_message(user_id, "تم التحقق من صحة الرابط بنجاح. يمكنك إرسال رسالتك.")
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("إرسال الرسالة", callback_data="send_message"))
            
            bot.send_message(user_id, "اضغط على زر إرسال الرسالة.", reply_markup=markup)
        elif status[0] == 2:
            
            
            bot.send_message(user_id, "تم التحقق من صحة الرابط بنجاح. تم خصم 100 نقطة من حسابك وإعادة تفعيل رابطك.")
            
            bot.send_message(user_id, status[1])
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("إرسال الرسالة", callback_data="send_message"))
            
            bot.send_message(user_id, "اضغط على زر إرسال الرسالة.", reply_markup=markup)
        elif status[0] == 3:
            
            
            bot.send_message(user_id, "تم التحقق من صحة الرابط بنجاح. تم إضافة نقاطك إلى حسابك وإلغاء تفعيل رابطك.")
            
            bot.send_message(user_id, status[1])
            
            bot.send_message(user_id, "لا يمكنك إرسال رسالتك لأنك لا تمتلك عدد كافي من النقاط. يجب أن يكون لديك 100 نقطة على الأقل.")
        elif status[0] == 4:
            
            
            bot.send_message(user_id, "الرابط غير مفعل. أدخل رابط صحيح.")
            bot.register_next_step_handler(message, handle_link)
        else:
            
            
            bot.send_message(user_id, "حصل خطأ ما في التحقق من الرابط.")
            bot.send_message(user_id, status)
    except AssertionError as e:
        
        bot.send_message(user_id, e.args[0])
        bot.send_message(user_id, "أعد إدخال رابط صحيح.")
        bot.register_next_step_handler(message, handle_link)
    
bot.polling()