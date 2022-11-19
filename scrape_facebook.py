# Selenium related libraries
import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup
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
url_housing_rotterdam = "https://www.facebook.com/groups/apartmentshousingrotterdam?sorting_setting=CHRONOLOGICAL_LISTINGS"

driver.get(url_housing_rotterdam) 
sleep(4) 

soup = BeautifulSoup(driver.page_source, "html.parser")
all_posts=soup.find_all("div", class_="x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z")

for post in all_posts:
    since = post.find("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h").text
    description = post.find("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h").text
    print(since, "\n", description)
    
len(all_posts)    
    