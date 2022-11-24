#! /bin/bash
# Colors for output
RED='\033[0;31m'
Green='\033[0;32m'
BCyan='\033[1;36m'
NC='\033[0m' # No color

cd "C:\Users\Home\Desktop\python\scrape_housing_listings"

printf "Ye old apartment hunt is starting\n\n Scraping the listings..."

py download_data.py

printf "\n\nScraped! Now off to generate the report!"

Rscript.exe knit_report.R

printf "\n\nDone!"

explorer format_report.html