import requests
import re
from pandas import DataFrame
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

funda_url = "https://www.funda.nl/huur/rotterdam/0-900/sorteer-datum-af/"

chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
""" chrome_options.add_argument("headless") """

driver = webdriver.Chrome(chrome_options=chrome_options)
sleep(3)
driver.get(funda_url)
sleep(5)
cookies = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))).click()

listing_element = driver.find_element(By.XPATH, '//*[@id="content"]/form/div[3]/div[2]/div[3]')
listing_html    = listing_element.get_attribute('innerHTML')
