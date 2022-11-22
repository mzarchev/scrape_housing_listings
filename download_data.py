from scrape_pararius import scrape_pararius_url
from scrape_kamernet import scrape_kamernet_url
from scrape_interhouse import scrape_interhouse_url

# Pararius
df_pararius = scrape_pararius_url("https://www.pararius.com/apartments/rotterdam/0-900")
df_pararius.to_csv("pararius_listings.csv", header=True, index=False)

# Kamernet
df_kamernet = scrape_kamernet_url("https://kamernet.nl/en/for-rent/rooms-rotterdam")
df_kamernet.to_csv("kamernet_listings.csv", header=True, index=False)

df_interhouse = scrape_interhouse_url("https://interhouse.nl/huurwoningen/?search_terms=Rotterdam&maximum_price=900&number_of_results=20&sort=date-desc&display=list")
df_interhouse.to_csv("interhouse_listings.csv", header=True, index = False)
