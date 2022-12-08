#! /bin/bash
# Colors for output
RED='\033[0;31m'
Green='\033[0;32m'
BCyan='\033[1;36m'
NC='\033[0m' # No color

cd "C:\Users\Home\Desktop\python projects\scrape_housing_listings"

printf "Ye olde ${BCyan}apartment hunt${NC} is starting\n\n    ${NC}Scraping${NC} the listings..."

py download_data.py

printf "\n\n${Green}Scraped!${NC} Now off to generate the report!\n\n\n"

Rscript.exe knit_report.R

printf "\n\n${Green}Done!${NC}"

sleep 2

explorer format_report.html

sleep 5