import requests
import re
from pandas import DataFrame
from bs4 import BeautifulSoup

def scrape_kamernet_url(kamernet_url):
    
    page = requests.get(kamernet_url)
    soup = BeautifulSoup(page.content, "html.parser")

    listings = soup.find_all("div", class_="rowSearchResultRoom col s12 m6 l4")

    listings_dict = {"name":  [],
                    "type":  [],
                    "days_ago": [],
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
        
        # Title
        name = listing.find("a", class_="tile-title truncate").text
        # Type
        type = listing.find("div", class_="tile-room-type").text
        type = re.findall(r"[A-Z].+(?=[\r])", type)
        # Price numeric
        price = listing.find("div", class_="tile-rent").text
        price = int(re.findall(r'\d+', price)[0])
        # Area square meters
        area = listing.find("div", class_="tile-surface").text
        # area = int(re.findall(r'\d+', area)[0]) # If converted to numeric
        # Main image
        img = listing.find("img", class_="lazyload")["src"]
        # Availability
        availability = listing.find("div", class_="left").text
        availability = " until ".join(re.findall("\d+-\d+-'?\d+", availability))
        # Link
        url = listing.find("a", class_="tile-title truncate")["href"]
        # When posted (sometimes undeclared)
        
        since = listing.find("div", class_="right tile-dateplaced").text
        since = re.findall(r"\d+[a-z]+", since)[0]
        # How many days ago
        if re.search(r"\d+h", since):
            days_ago = 0
        elif re.search(r"\d+d", since):
            days_ago = re.findall(r"\d+(?=d)", since)[0]
        elif re.search(r"\d+w", since):    
            weeks_ago = re.findall(r"\d+(?=w)", since)[0]
            days_ago = int(weeks_ago) * 7

        # Go into posting and extract more details
        soup_listing = BeautifulSoup(requests.get(url).content, "html.parser")    
        # Number of rooms
        try:
            rooms = soup_listing.find("span", class_="rooms-numbers").text
            rooms = rooms.replace("\r\n", "").strip()
        except:
            rooms = "Number of rooms unlisted"
        # Are utilities included
        utilities = soup_listing.find("div", class_="gwe").text.replace("p/m | ", "")
        # Description
        description = soup_listing.find("div", class_="col s12 room-description desc-special-text").text
        description = description.replace("\r\n", "").strip()
        
        listings_dict["name"].append(name)
        listings_dict["type"].append(type)
        listings_dict["days_ago"].append(days_ago)
        listings_dict["price"].append(price)
        listings_dict["utilities"].append(utilities)
        listings_dict["area"].append(area)
        listings_dict["rooms"].append(rooms)
        listings_dict["availability"].append(availability)
        listings_dict["description"].append(description)
        listings_dict["url"].append(url)
        listings_dict["img"].append(img)

    return(DataFrame(listings_dict))
