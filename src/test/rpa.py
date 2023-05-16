import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()


def _login(driver: webdriver, username: str, password: str, login_url: str):
    """
    Login to Price Movers Website.
    :param driver: Chrome webDriver
    :param username: Username for Login
    :param password: Password for Login
    :param login_url: Login URL
    :return:
    """
    # Find and Fill in Username and Password Forms
    driver.get(login_url)
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-primary ok']"))).click()
    time.sleep(15)
    print("Entering Login Details for Website.")
    user_name = driver.find_element_by_id("email")
    user_name.clear()
    user_name.send_keys(username)

    pass_word = driver.find_element_by_id("password")
    pass_word.clear()
    pass_word.send_keys(password)

    # Find and Click Login/Submit
    login = driver.find_element_by_id("login")
    WebDriverWait(driver, 20).until(EC.visibility_of(login))
    driver.execute_script("arguments[0].click();", login)
    print("Login Done.")


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--remote-debugging-port=9222")
    # options.add_argument("--disable-dev-shm-usage")
    preferences = {
        "profile.default_content_settings.popups": 0,
        "download.default_directory": r'C:\Users\aitembo\Downloads\Chrome',
        "directory_upgrade": True,
        'profile.default_content_setting_values.automatic_downloads': 1
    }
    options.add_experimental_option('prefs', preferences)
    binary_path = r"C:\Users\aitembo\Downloads\chromedriver_win32\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=binary_path, options=options)
    username = os.environ.get('TRUVU_USERNAME')
    password = os.environ.get('TRUVU_PWD')
    login_url = "https://www.mytruvu360.com/truvu360_web/securityController/loginPage"
    _login(driver, username, password, login_url)
    time.sleep(10)
    print("Navigating Website to get Exported Data.")
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//i[@class='jstree-icon jstree-ocl']"))).click()
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//body/div[@id='body']/div[@id='middle']/div[@class='row']/div[@id='main-left']/div[@class='card']/div[@class='card-body']/div[@id='asset-tree']/ul[@role='group']/li[@id='root489534']/ul[@role='group']/li[@id='rootLevel489544']/i[1]"))).click()
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@id='level856707_anchor']"))).click()
    time.sleep(5)
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//i[@class='fas fa-file-export fa-2x']"))).click()
    time.sleep(2)
    print("Picking Date Time Range.")
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='export-samples-date-range']"))).click()
    # WebDriverWait(driver, 20).until(
    #     EC.element_to_be_clickable((By.XPATH,
    #                                 "(//li[@data-range-key='Yesterday'][normalize-space("
    #                                 ")='Yesterday'])[2]"))).click()
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "(//li[contains(text(),'Last 7 Days')])[2]"))).click()
    time.sleep(2)
    print("Clicking Export.")
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='button'][normalize-space()='Export']"))).click()
    print("Allow 30 seconds to Allow Files to Export.")
    time.sleep(30)
    driver.quit()
    print("Done.")


