from telethon.sync import TelegramClient 
import telethon
from time import sleep
import sqlite3 


client = TelegramClient("session_name3", api_id="25153583", api_hash="35543407ec1e319a3927f267183adb5d")


con = sqlite3.connect("tutorial.db")


cur = con.cursor()


cur.execute("CREATE TABLE IF NOT EXISTS list (id INTEGER PRIMARY KEY, users TEXT, message TEXT, times INTEGER, sent INTEGER)")




def update_list(id, times, sent):
    cur.execute("UPDATE list SET times = ?, sent = ? WHERE id = ?", (times, sent, id))
    con.commit()


def delete_list(id):
    cur.execute("DELETE FROM list WHERE id = ?", (id,))
    con.commit()


def send_messages():
    
    client.connect()
    print("start")
    
    if not client.is_user_authorized():
        phone = "+371 213 51000"
        client.send_code_request(phone, force_sms=False)
        value = input("Enter login code: ")
        try:
            me = client.sign_in(phone, code=value)
        except telethon.errors.SessionPasswordNeededError:
            password = ("0000000")
            me = client.sign_in(password=password)

    
    list_index = 0

    
    cur.execute("SELECT * FROM list")
    lists = cur.fetchall()

    
    while list_index < len(lists):
        
        data = lists[list_index]
        print(list_index)
        id = data[0]
        users = data[1].split(",") 
        message = data[2]
        times = data[3]
        sent = data[4]

        
        if times > 0:
            
            for user in users:
                try:
                    client.send_message(user,message)
                    
                    print(f'Message sent successfully {list_index}')
                    
                    sent += 1  
                    
                    times -= 1
                    sleep(1.5)
                    update_list(id, times, sent)
                except telethon.errors.rpcerrorlist.ChatWriteForbiddenError:
                    print(f"\n\nerror in: {user}\n\n")
                except telethon.errors.rpcerrorlist.UserBannedInChannelError:
                    print(f"\n\nerror Channel: {user}\n\n")
                except ConnectionError:
                    print(f"\n\nConnection error will be skipped when\nusername: {user}\n\n")
                    return
                except ValueError:
                    print(f'\n\nValueError: No user has "{user}" as username\n\n')
            sleep(50)

        else:
            
            delete_list(id)

        
        list_index += 1

    client.disconnect()


while True:
        send_messages()