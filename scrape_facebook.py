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

## Opening browser
# Diasble onotification
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
#chrome_options.add_argument("headless")

# Open browser and go to facebook.com
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.facebook.com")
driver.maximize_window()
sleep(2)

## Logging in
# Accept cookies
cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="_42ft _4jy0 _9xo7 _4jy3 _4jy1 selected _51sy"]'))).click()
# Get credentials
with open("profile.txt") as f:
    email_str, passw = [line for line in f.readlines()]
    email_str = email_str.replace('\n', '')

# Loggin page    
email=driver.find_element(by="id", value="email")
email.send_keys(email_str)
password=driver.find_element(by="id", value ="pass")
password.send_keys(passw)
sleep(1)
login=driver.find_element(by="name", value="login")
login.click()
sleep(2)

# Get to group
url_housing_rotterdam = "https://www.facebook.com/groups/1085601721566069/?hoisted_section_header_type=recently_seen&multi_permalinks=5422870601172471"

driver.get(url_housing_rotterdam) 
sleep(4) 