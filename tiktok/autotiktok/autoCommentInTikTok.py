from pyautogui import *

from time import sleep
from pyperclip import copy
from random import choice

we = ["ويانا","معايا","معي","معانا","وياي","معنا"]
text = "سلام عليكم نحن محاربين ابتزاز اي شخص محتاج اي مساعدة يتواصل معنا على الخاص + الي عندة خبرة او يحس نفسة قادر على المساعدة وعندة وقت كذالك يتواصل معنا"
copy(text)

def message():
  arrow = locateCenterOnScreen("downArrow.png",confidence=0.7)
  click(arrow,duration=1)
  message = locateCenterOnScreen("message.png",confidence=0.7)
  click(message,duration=1)
  hotkey('ctrl', 'v')
  sleep(0.5)
  
  post = locateCenterOnScreen("post.png",confidence=0.8)
  moveTo(post,duration=0.5)
  sleep(1)
  doubleClick()
  i = 0
  
  while True:
    try:
      locateCenterOnScreen("errorMessage.png")
      _we = choice(we)
      _we_ = choice(we)
      text = f"سلام عليكم نحن محاربين ابتزاز اي شخص محتاج اي مساعدة يتواصل {_we} على الخاص + الي عندة خبرة او يحس نفسة قادر على المساعدة وعندة وقت كذالك يتواصل {_we_}"
      copy(text)
      xMessage,yMessage= locateCenterOnScreen("errorMessage_0.png",confidence=0.7)
      doubleClick(xMessage+100,yMessage,duration=0.5)
      click()
  
      hotkey('ctrl', 'v')
      sleep(0.5)
  
      post = locateCenterOnScreen("post.png",confidence=0.8)
      moveTo(post,duration=0.5)
      sleep(1)
      doubleClick()
      i = 0
    except:
      sleep(0.2)
    
    if i == 50:
      i = 0
      break
    else:
      i += 1

def reset():
  xStar,yStar=locateCenterOnScreen("star.png")
  click(xStar+200,yStar,duration=0.5)
  sleep(0.5)

  write("tiktok.com")
  sleep(0.5)

  hotkey("enter")
  sleep(0.5)

  x,y=size();centerScreen=x/2,y/2
  i = 0
  
  while True:
    try:
      locateCenterOnScreen("like.png")
      break
    except:
      sleep(1)
    if i == 10:
      exit()
    else:
      i += 1

  click(centerScreen)
  sleep(2)

while True:
  try:
    message()
  except Exception as e:
    open("logtik.txt","w").write(str(e))
    reset()
