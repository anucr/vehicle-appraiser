import requests
from bs4 import BeautifulSoup
import re
import csv
import time

def scrape_riyasewana_index(pages=3):
    """
    Expert data extraction engine for Riyasewana secondary automotive market.
    """
    print(f"Initializing data extraction engine for {pages} pages...")
    base_url = "https://riyasewana.com/search/cars"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    extracted_data = []
    
    for page in range(1, pages + 1):
        url = base_url if page == 1 else f"{base_url}?page={page}"
        print(f"Scraping Index Page {page}: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"Failed to fetch page {page}. HTTP Status: {response.status_code}")
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Target list items matching the vehicle card markup structure
            listings = soup.find_all('li', class_=lambda c: c and 'v-card' in c)
            
            for item in listings:
                # 1. Listing Title
                title_elem = item.select_one('.v-card-title a')
                title = title_elem.text.strip() if title_elem else "Unknown Title"
                
                # 2. Exact Price LKR
                price_elem = item.select_one('.v-card-price')
                raw_price = price_elem.text.strip() if price_elem else "0"
                # Strip out non-numeric characters (e.g., "Rs. 6,850,000" -> 6850000)
                clean_price_str = re.sub(r'[^\d]', '', raw_price)
                exact_price = int(clean_price_str) if clean_price_str else 0
                
                # Filter out items with price < 300,000 LKR (Mock/broken listings)
                if exact_price < 300000:
                    continue
                    
                # 3. Specification Log & 4. Manufacture Year
                # Riyasewana's updated structure places year in .v-card-year and specs in .v-card-meta
                year_elem = item.select_one('.v-card-year')
                year_text = year_elem.text.strip() if year_elem else ""
                
                # Extract 4-digit year using regex
                year_match = re.search(r'\b(19|20)\d{2}\b', year_text)
                manufacture_year = year_match.group(0) if year_match else "Unknown"
                
                # Extract structural log details (mileage, location, etc.)
                meta_elem = item.select_one('.v-card-meta')
                spec_log = meta_elem.text.strip() if meta_elem else "No specifications provided"
                
                # Replace the HTML middle dot separator with a cleaner pipe delimiter
                spec_log = spec_log.replace('\u00b7', ' | ')
                
                extracted_data.append({
                    "Listing Title": title,
                    "Exact Price LKR": exact_price,
                    "Specification Log": spec_log,
                    "Manufacture Year": manufacture_year
                })
                
        except Exception as e:
            print(f"Error scraping page {page}: {e}")
            
        # Polite crawl delay of 2 seconds to preserve data integrity and respect rate limits
        time.sleep(2)
        
    # Output to structured CSV
    output_filename = "sri_lankan_car_database.csv"
    if extracted_data:
        keys = ["Listing Title", "Exact Price LKR", "Specification Log", "Manufacture Year"]
        with open(output_filename, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(extracted_data)
        print(f"\nExtraction complete! Successfully compiled {len(extracted_data)} validated records to '{output_filename}'.")
    else:
        print("\nNo valid records extracted after applying filters.")

if __name__ == "__main__":
    scrape_riyasewana_index(pages=3)
