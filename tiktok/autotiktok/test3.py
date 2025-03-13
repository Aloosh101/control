from selenium import webdriver

def login(driver, username, password):
    driver.get("https://example.com/login")
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_id("login").click()

def save_session(driver):
    driver.get("https://example.com/session")
    session_id = driver.get_cookie("SESSIONID")
    with open("session.txt", "w") as f:
        f.write(session_id)

def open_session(driver):
    with open("session.txt", "r") as f:
        session_id = f.read()
    driver.get("https://example.com/")
    driver.add_cookie({"name": "SESSIONID", "value": session_id})

if __name__ == "__main__":
    driver = webdriver.Chrome()
    username = "username"
    password = "password"

    login(driver, username, password)
    save_session(driver)

    driver.close()

    # Run the code again

    driver = webdriver.Chrome()
    open_session(driver)
