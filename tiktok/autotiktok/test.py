from selenium import webdriver
from time import sleep

# إنشاء متصفح
driver = webdriver.Chrome()

# الانتقال إلى موقع الويب
driver.get("https://www.facebook.com")

# العثور على مربع إدخال اسم المستخدم
username_input = driver.find_element("id","email")

# إدخال اسم المستخدم
username_input.send_keys("your_username")
sleep(100)

# العثور على مربع إدخال كلمة المرور
password_input = driver.find_element_by_id("pass")

# إدخال كلمة المرور
password_input.send_keys("your_password")

# النقر على زر تسجيل الدخول
login_button = driver.find_element_by_id("loginbutton")
login_button.click()

# الانتظار حتى يتم تحميل الصفحة
driver.implicitly_wait(10)

# حفظ الجلسة والكوكيز
cookies = driver.get_cookies()

# إغلاق المتصفح
driver.quit()
