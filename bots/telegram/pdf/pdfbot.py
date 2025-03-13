import telebot
from PIL import Image
import io
import os
import tempfile
import threading
bot = telebot.TeleBot("123456789:wsedrtyuiolprtyu")

button = telebot.types.InlineKeyboardButton("نعم", callback_data="yes")
convert_button = telebot.types.InlineKeyboardButton("تحويل", callback_data="convert")
cancel_button = telebot.types.InlineKeyboardButton("الغاء", callback_data="cancel")

user_state = False
user_images = []
user_message = None
user_timer = None

TIMEOUT = 300 



@bot.message_handler(commands=['start'])
def start(message):
    global user_state, user_images, user_message, user_timer
    user_state = False
    user_images = []
    user_message = None
    user_timer = None

    bot.send_message(message.chat.id, "مرحبا ، أنا BOT يمكنه تحويل الصور إلى ملفات PDF. هل تريدني أن أفعل ذلك؟", reply_markup=telebot.types.InlineKeyboardMarkup().add(button))

@bot.callback_query_handler(func=lambda call: call.data == "yes")
def convert(call):
    global user_state, user_images, user_message, user_timer
    user_state = True
    user_images = []
    bot.send_message(call.message.chat.id, "حسنا ، من فضلك أرسل لي الصورة أو مجموعة من الصور.")
    user_timer = threading.Timer(TIMEOUT, timeout, args=[call.message.chat.id])
    user_timer.start()

@bot.callback_query_handler(func=lambda call: call.data == "convert")
def send_pdf(call):
    global user_state, user_images, user_message, user_timer
    try:
        if user_state and user_images:
            pdf_list = []

            for image in user_images:
                pdf = Image.open(io.BytesIO(image)).convert("RGB")
                pdf_list.append(pdf)

            pdf_bytes = io.BytesIO()
            pdf_list[0].save(pdf_bytes, format="PDF", save_all=True, append_images=(pdf_list[1:]))

            pdf_name = "{}.pdf".format(call.message.chat.id)
            with tempfile.TemporaryDirectory() as temp_dir: 
                pdf_path = os.path.join(temp_dir, pdf_name)
                with open(pdf_path, "wb") as pdf_file:
                    pdf_file.write(pdf_bytes.getvalue())

                with open(pdf_path, "rb") as pdf_file:
                    bot.send_document(call.message.chat.id, pdf_file)

            bot.send_message(call.message.chat.id, "تم. إذا كنت تريد استخدام الروبوت مرة أخرى ، فاضغط على /start.")
            reset()
        else:
            bot.send_message(call.message.chat.id, "من فضلك ، أرسل لي بعض الصور أولا قبل الضغط على زر التحويل.")
    except Exception as e:
        print(e)
        bot.send_message(call.message.chat.id, "فشل تحويل الصورة أو مجموعة الصور. يرجى التأكد من أنها ليست تالفة أو ليست ملفا أو نصا. إرسال الصور فقط. إذا استمر هذا الخطأ ، فاتصل بالمبرمج لحل المشكلة أعد تشغيل الروبوت /start")
        reset()

@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def cancel(call):
    global user_state, user_images, user_message, user_timer
    bot.send_message(call.message.chat.id, "لقد ألغيت التحويل. إذا كنت تريد استخدام الروبوت مرة أخرى ، فاضغط على /start.")
    reset()

@bot.message_handler(content_types=['photo', 'text'])
def receive_image(message):
    global user_state, user_images, user_message, user_timer
    try:
        if user_state:
            photo = bot.get_file(message.photo[-1].file_id)
            image = bot.download_file(photo.file_path)
            user_images.append(image)
            if not user_message:
                user_message = bot.send_message(message.chat.id,
                                                f"حصلت على {len(user_images)} صور/ة. اضغط على زر تحويل أو إلغاء عند الانتهاء.",
                                                reply_markup=telebot.types.InlineKeyboardMarkup().row(convert_button,
                                                                                                  cancel_button))
            else:
                bot.edit_message_text(f"حصلت على {len(user_images)} صور/ة. اضغط على زر تحويل أو إلغاء عند الانتهاء.",
                                      message.chat.id,
                                      message_id=user_message.message_id,
                                      reply_markup=telebot.types.InlineKeyboardMarkup().row(convert_button,
                                                                                            cancel_button))
                restart_timer(message.chat.id)
        else:
            bot.send_message(message.chat.id, "من فضلك ، ابدأ البوت أولا بالضغط على /start.")
    except:
        bot.send_message(message.chat.id, "فشل في استلام الصورة. يرجى التأكد من أنه ليس تالفا أو ليس ملفا أو نصا. إرسال الصور فقط. إذا استمر هذا الخطأ ، فاتصل بالمبرمج لحل المشكلة \n\n أعد تشغيل الروبوت /start")

def timeout(chat_id):
    global user_state, user_images, user_message, user_timer
    bot.send_message(chat_id, "لقد كنت غير نشط لمدة 5 دقائق. تم إلغاء التحويل. إذا كنت تريد استخدام الروبوت مرة أخرى ، فاضغط على /start.")
    reset()

def reset():
    global user_state, user_images, user_message, user_timer
    user_state = False
    user_images = []
    user_message = None
    if user_timer:
        user_timer.cancel()
        user_timer = None

def restart_timer(chat_id):
    global user_state, user_images, user_message, user_timer
    if user_timer:
        user_timer.cancel()
        user_timer = threading.Timer(TIMEOUT, timeout, args=[chat_id])
        user_timer.start()


bot.polling()
