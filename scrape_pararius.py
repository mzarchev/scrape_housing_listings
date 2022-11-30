import re
from pandas import DataFrame
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime, timedelta
from selenium import webdriver

def scrape_pararius_url(pararius_url, check_days_back=1):

    browser = webdriver.Chrome()
    browser.get(pararius_url)
    sleep(3)
    # Get static HTML file
    page = browser.page_source
    soup = BeautifulSoup(page, "html.parser")


    # Extract all listings
    result_listings = soup.find_all("li", class_="search-list__item search-list__item--listing")

    # Prepare dictionary for listings
    listings_dict = {"name":  [],
                    "type":  [],
                    "since": [],
                    "days_ago": [],
                    "price": [],
                    "area":  [],
                    "rooms": [],
                    "img":   [],
                    "url":   [],
                    "lat":   [],
                    "lon":   [],
                    "description" : [],
                    "availability": []
                    }

    # Loop through listings
    for listing in result_listings:

        # Title
        title = listing.find("a", class_="listing-search-item__link listing-search-item__link--title")
        # Type of listing (studio, apartment)
        type = re.findall(r'[a-zA-Z]+' ,title.text)[0]
        # Name of the street listing
        name = re.findall(r'[a-zA-Z]+' ,title.text)[1]
        # Extract price numeric
        price = listing.find("div", class_="listing-search-item__price")
        price = int(re.findall(r'\d+', price.text)[0])
        # Area square feet
        area  = listing.find("li", class_="illustrated-features__item illustrated-features__item--surface-area")
        # Number of rooms
        rooms = listing.find("li", class_="illustrated-features__item illustrated-features__item--number-of-rooms")
        # Main image
        img = listing.find("img")["src"]
        # Get the url (partial, needs to be combined with original url)
        url_temp = listing.find("a", class_="listing-search-item__link listing-search-item__link--title")["href"]
        url_full = "https://www.pararius.com" + url_temp
        browser.get(url_full)
        """ sleep(3) """
        ## Go to the listing details url and extract info from there
        listing_soup = BeautifulSoup(browser.page_source, "html.parser")
        # Availability (available, under auction, etc)
        availability = listing_soup.find("dd", class_="listing-features__description listing-features__description--acceptance").text
        availability = availability.replace("\n", "")
        # The full description
        description  = listing_soup.find("div", class_="listing-detail-description__content").text
        description  = description.replace("\n\nDescription\n", "")
        # Map coordinates
        map_element = listing_soup.find("div", class_="page__wrapper page__wrapper--map").decode_contents()
        lat = re.findall(r'(?<=latitude=")\d+[.]\d+', map_element)
        lat = float(lat[0])
        lon = re.findall(r'(?<=longitude=")\d+[.]\d+', map_element)
        lon = float(lon[0])
        
        # Time variables
        # Offered since
        since = listing_soup.find("dd", class_="listing-features__description listing-features__description--offered_since").text
        since = since.replace("\n", "")
        # Convert weeks to date 
        if re.search(r"\d+ weeks", since):     
            weeks_temp = int(re.findall(r'\d+', since)[0])
            date_temp = datetime.today() - timedelta(weeks=weeks_temp)
            since = f"{date_temp.day}-{date_temp.month}-{date_temp.year}"
        # Convert months to date
        elif re.search(r"\d+[+]? months", since):
            months_temp = int(re.findall(r'\d+', since)[0])
            date_temp = datetime.today() - timedelta(weeks=months_temp*4)
            since = f"{date_temp.day}-{date_temp.month}-{date_temp.year}"
        # Function to get how many days since listing
        def days_since(date_string: str) -> int:
            date = datetime.strptime(date_string, "%d-%m-%Y")
            diff = datetime.today() - date
            return(diff.days) 
        # Get how many days ago listing was posted
        days_ago = days_since(since)
        
        if days_ago > check_days_back: break

        # Store everything in a dictionary    
        listings_dict["name"].append(name)
        listings_dict["type"].append(type)
        listings_dict["since"].append(since)
        listings_dict["days_ago"].append(days_ago)
        listings_dict["price"].append(price)
        listings_dict["area"].append(area.text)
        listings_dict["rooms"].append(rooms.text)
        listings_dict["lat"].append(lat)
        listings_dict["lon"].append(lon)
        listings_dict["availability"].append(availability)
        listings_dict["description"].append(description)
        listings_dict["url"].append(url_full)
        listings_dict["img"].append(img)

    browser.close()
    df_listings = DataFrame(listings_dict)
    return(df_listings)