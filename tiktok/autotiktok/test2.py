from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By


def login(email:str,password:str,driver):
    driver.get("https://www.tiktok.com/login/phone-or-email/email")
    
    #add email
    usernameInput = driver.find_element(By.NAME,"username")
    usernameInput.send_keys(email)

    #add password
    passwordInput = driver.find_element(By.CLASS_NAME,"tiktok-wv3bkt-InputContainer")
    passwordInput.send_keys(password)

    #click login
    loginSubmit = driver.find_element(By.CLASS_NAME,"tiktok-11sviba-Button-StyledButton")
    loginSubmit.click()

def openVideo(driver):
    driver.get("https://www.tiktok.com/")
    #click the video 
    videoClick = driver.find_element(By.CLASS_NAME,"css-41hm0z")
    videoClick.click()

def commentsAndScroll(message:str,driver):
    
    #write comment
    commentsInput = driver.find_element(By.CLASS_NAME,"css-jvtqsz-DivCommentContainer")
    commentsInput.send_keys(message)

    #click the post button
    postComment = driver.find_element(By.CLASS_NAME, "css-1s8nwgg-DivPostButton")
    postComment.click()

    #scroll down for new video
    scrollDown = driver.find_element(By.CLASS_NAME,"css-41d2fr-ButtonBasicButtonContainer-StyledVideoSwitch")
    scrollDown.click()



driver = webdriver.Chrome()



login("x10101001010010@gmail.com","x10x1x100x1x1000x0?",driver)
sleep(60)
openVideo(driver)
commentsAndScroll("hi",driver)