import requests
import re
from pandas import DataFrame
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import sleep
# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_interhouse_url(url_interhouse):

    ## Selenium
    # Don't open a chrome window run in background
    options = Options()
    options.add_argument("headless")
    # Open page
    driver = webdriver.Chrome(options=options)
    driver.get(url_interhouse)
    sleep(3)
    # Close cookies
    cookies = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]'))).click()
    sleep(3)
    # Get the source
    page = driver.page_source

    # Extract listings from source
    soup = BeautifulSoup(page, "html.parser")
    listings = soup.find_all("div", class_="c-result-item building-result c-result-item--horizontal")

    listings_dict = {"name":  [],
                    "type":  [],
                    "status": [],    
                    "price": [],
                    "area":  [],
                    "rooms": [],
                    "img":   [],
                    "url":   [],
                    "utilities": [],
                    "description": [],
                    "availability": []
                    }

    for listing in listings:
        
        # Most of the listing info is kept in a table that needs to get looped through
        info_table = listing.find_all("p", class_="c-result-item__data-value")

        type, availability, area, status, \
        bedrooms, furniture = [value.text for value in info_table]
        
        # Remove garages
        if (type == "Garage"): pass
        
        # Title 
        name = listing.find("span", class_="c-result-item__title-address").text
        # Price numeric
        price = listing.find("p", class_="c-result-item__price-label").text
        price = int(re.findall(r'\d+', price)[0])
        # Are utilities included
        utilities = listing.find("small", class_="c-result-item__price-notes").text
        # Link
        url = listing.find("div", class_="c-result-item__image").find("a")["href"]
        # Image
        img = listing.find("div", class_="c-result-item__image").find("a")["style"]
        img = re.findall("(?<=[(]).+(?=[)])", img)[0]
        
        # Go in url to extract description
        listing_soup = BeautifulSoup(requests.get(url).content)
        description = listing_soup.find("div", class_="building-description").text

        listings_dict["name"].append(name)
        listings_dict["type"].append(type)
        listings_dict["price"].append(price)
        listings_dict["utilities"].append(utilities)
        listings_dict["area"].append(area)
        listings_dict["rooms"].append(bedrooms)
        listings_dict["availability"].append(availability)
        listings_dict["description"].append(description)
        listings_dict["url"].append(url)
        listings_dict["img"].append(img)
        listings_dict["status"].append(status)
        
    df_untidy = DataFrame(listings_dict)
    df_interhouse = df_untidy[(df_untidy.status == "Beschikbaar") & (df_untidy.type != "Garage")]
    
    return(df_interhouse)