
from telethon import TelegramClient
from time import sleep
import telethon
import asyncio
import sqlite3
from telethon.tl.functions.account import CheckUsernameRequest, UpdateUsernameRequest
print("المطور: @ \n\n")

async def now_account(phone_number,session_number):
    client = TelegramClient(
    str(session_number),
    api_id="12345678",
    api_hash="123456789o"
    )

    
    await client.connect()
    
    await client.send_code_request(phone_number, force_sms=False)
    value = input("\n\nادخل كود تسجيل الدخول: ")
    attempts = 0 
    try:
        me = await client.sign_in(
        phone_number, 
        code=value
        )
    except telethon.errors.SessionPasswordNeededError:
        password = input("\n\nادخل كلمة سر التحقق الثنائي: ")
        me = await client.sign_in(
        password=password
        )
    except telethon.errors.PhoneCodeInvalidError:
        print("\n\nرمز التحقق غير صالح")
        attempts += 1 
        if attempts < 3: 
            value = input("\n\nادخل كود تسجيل الدخول مرة أخرى: ")
            me = await client.sign_in(
            phone_number,
            code=value
            )
        else: 
            print("\n\nلقد تجاوزت الحد المسموح من المحاولات")
    finally:    
        if client.is_user_authorized():
            print("تم تسجيل الدخول بنجاح")
        else:
             print("لم يتم تسجيل الدخول")

        
        await client.disconnect()

async def check_and_change_username(username,session_number):
  client = TelegramClient(
    str(session_number),
    api_id="20080380",
    api_hash="1bf64fab6d33e1f58616eadca0f3e507"
  )
  
  await client.connect()
  
  try:
    
    result = await client(CheckUsernameRequest(username))
    if result:
      
      await client(UpdateUsernameRequest(username))
      print("\n\nاسم المستخدم تغير بنجاح\n\n")
    else:
      print("\n\nاسم المستخدم غير متوفر\n\n")
  
  except telethon.errors.FloodWaitError as e:
    print(f"\n\nانتظر {e.seconds} ثانية قبل إعادة المحاولة\n\n")
  except telethon.errors.UsernameInvalidError:
    print("\n\nاسم المستخدم غير صالح\n\n")
  except telethon.errors.UsernameOccupiedError:
    print("\n\nاسم المستخدم محجوز\n\n")
  
  await client.disconnect()


while True:
    
    enter = input(
            "ادخل 1 لاضافه رقم جديد\n" +
            "ادخل 2 لاضافه يوزرات للارقام\n" +
            "ادخل 3 لاظهار الارقام مع اليوزرا\n" +
            "دخل 4 للايقاف: "
            )
    
    enter = str(enter.strip())
    
    try:
        
        if enter == "1":
                print(
                "ادخل رقم هاتفك بهذة الصيغة\n"+
                "+9640000000000\n\n\n\n"
                )
                
                
                phone_number = input("ادخل رقم هاتفك بهذة الصيغة\n"+ "+9640000000000\n\n\n\n" + "ادخل رقم هاتفك هنا\n " +"ادخل رقم 1 اذا تريد الرجوع الى الصفحة الرئيسية: " )
                
                if str(phone_number) == "1":
                    
                    print("\n\n\n\n")
                    break
                
                else:
                    
                    try:
                        con = sqlite3.connect("./sayku.db")
                        cur = con.cursor()
                        
                        cur.execute("SELECT id FROM sessions_number WHERE rowid=1")
                        session_number = cur.fetchone()
                        
                        if session_number is None:
                            
                            cur.execute("INSERT INTO sessions_number (id) VALUES (1)")
                            session_number = 1
                        
                        else:
                            
                            session_number = session_number[0] + 1
                            cur.execute("UPDATE sessions_number SET id=? WHERE rowid=1", (session_number,))
                        
                        cur.execute("INSERT INTO accounts (id,phone_number,username) VALUES (?,?,?)",( session_number, phone_number, "" ) )
                        
                        con.commit()
                        
                        con.close()
                        
                        asyncio.run(now_account(phone_number=phone_number,session_number=session_number))
                        
                        print("\n\nتم اضافة الحساب\n\n")
                        break
                    
                    except:
                        
                        print('\n\nحدث خطأ في الاتصال بقاعدة البيانات. يرجى التأكد من أن ملف sayku.db موجود في نفس المجلد.\n\n')
                        break
                    
                    
        
        elif enter == "2":
                try:
                    
                    con = sqlite3.connect("./sayku.db")
                    
                    cur = con.cursor()
                    
                    cur.execute("SELECT id FROM sessions_number")
                    session_number = list(cur.fetchone())

                    
                    for x in range(1, (int(session_number[0])+1)): 
                        try:                
                            
                            cur.execute("SELECT username FROM accounts WHERE id = ?", (x,))
                            user = cur.fetchone()
                            
                            if str(user) == "('',)":
                                username = input("اكتب اليوزر الذي تريد اضافته: ")
                                
                                cur.execute('UPDATE "accounts" SET "username" = ? WHERE id = ?',(
                                username,
                                x
                                )
                                )
                                cur.execute("COMMIT")
                                
                                con.close
                                
                                asyncio.run(check_and_change_username(username,x))
                                break
                            elif int(x) == int(session_number[0]):
                                print("\n\nكل الارقام مستخدمه\n\n")
                                break
                            else:
                                
                                continue
                        except:
                            print('\n\nانت متاكد انك اضفت ارقام؟ اذا تكرر هذا الخطا اتصل بلمبرمج\n\n')
                except:
                    print('\n\nحدث خطأ في الاتصال بقاعدة البيانات. يرجى التأكد من أن ملف sayku.db موجود في نفس المجلد.\n\n')
        elif enter == "3":
                
                con = sqlite3.connect("./sayku.db")
                cur = con.cursor()
                print("\n\nهذة هي البيانات:\n\n")
                
                cur.execute("SELECT phone_number,username FROM accounts")
                
                rows = list(cur.fetchall())
                
                con.close()
                for row in rows:
                    print(row[0] + ": " + row[1] + "\n")
                
            
        elif enter == "4":
            print("تم الايقاف")
            break
        else:
            print("\n\nالرجاء التحقق من ادخال احدى الارقام من 1 الى 4\n\n")
    except:
        print("\n\nلا يسمح بستخدام الاحرف\n\n")