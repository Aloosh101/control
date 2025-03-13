import telebot

def download_audio_data(url: str):
    from pytube import YouTube
    
    from io import BytesIO
    bytes_io = BytesIO()

    youtube = YouTube(url)
    youtube.streams.get_audio_only().stream_to_buffer(bytes_io)
    
    data = bytes_io.getvalue()
    bytes_io.close()
    
    return data

bot = telebot.TeleBot(token="6930433650:AAG0L_T6KuM8DsqgdvzEKPRR47KHr6N3zdE")
bot.send_audio()