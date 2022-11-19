from scrape_pararius import scrape_pararius_url

# Pararius
df_pararius = scrape_pararius_url("https://www.pararius.com/apartments/rotterdam/0-900")
df_pararius.to_csv("pararius_listings.csv")