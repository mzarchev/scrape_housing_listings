# Selenium related libraries
import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from webdrivermanager.chrome import ChromeDriverManager

# Misc
from time import sleep

# Diasble onotification
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
#chrome_options.add_argument("headless")

# Open browser and go to facebook.com
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.facebook.com")
driver.maximize_window()
sleep(2)

# Accept cookies
cookies = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="_42ft _4jy0 _9xo7 _4jy3 _4jy1 selected _51sy"]'))).click()
# Get credentials
with open("profile.txt") as f:
    email, passw = [line for line in f.readlines()]
    email = email.replace('\n', '')
    #passw = f.readlines()[1]