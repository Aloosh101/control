from telethon.sync import TelegramClient
from time import sleep
import sys
import sqlite3
from telethon.tl.functions.messages import StartBotRequest
import re
class bot():
    def check_the_link(link: str,required_points: int):
        client = TelegramClient("bot", api_id="1234567", api_hash="12345678")
        
        client.start()
        params = link.split('=')[-1] 
        request = StartBotRequest('zmmbot', 'zmmbot', params) 
        result = client(request) 
        sleep(0.5)
        message = client.get_messages('zmmbot')[0] 
        pattern = r'\d+' 
        matches = re.findall(pattern, message.text) 
        try:
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
        except:
            e = sys.exc_info()[0] 
            print(e) 
            return ("لقد حصل خطا ما\nراسل المبرمج ان تكررت المشكلة لحلها باقرب وقت\n المبرمج: @mr_code_101")
        
        client.disconnect()
    
    def add_list(users, message, times):
        con = sqlite3.connect("tutorial.db")
        
        cur = con.cursor()
        
        users_str = ",".join(users)
        cur.execute("INSERT INTO list (users, message, times, sent) VALUES (?, ?, ?, 0)", (users_str, message, times))
        con.commit()
        con.close()