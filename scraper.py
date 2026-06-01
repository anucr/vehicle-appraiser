import requests
import json
import re
import time

def scrape_local_market_prices():
    # If streamlit is running, we can import it locally
    try:
        import streamlit as st
        st.write("🔄 Initializing Live Web Scraper Connection...")
    except:
        print("Initializing Live Web Scraper Connection...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # Mapping search term to clean database key
    target_models = {
        "alto": "Suzuki Alto",
        "wagon r": "Suzuki Wagon R",
        "axio": "Toyota Axio",
        "vezel": "Honda Vezel",
        "prius": "Toyota Prius"
    }
    
    scraped_market_data = {}
    
    for model_query, model_name in target_models.items():
        search_url = f"https://riyasewana.com/search/{model_query.replace(' ', '-')}"
        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            if response.status_code != 200:
                continue
                
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            listings = soup.find_all('li', class_=lambda c: c and 'v-card' in c)
            
            prices = []
            for item in listings[:8]:
                price_text = item.find(class_='v-card-price')
                if price_text:
                    numeric_price = re.sub(r'[^\d]', '', price_text.text)
                    if numeric_price:
                        prices.append(float(numeric_price))
            
            if prices:
                avg_market_price = sum(prices) / len(prices)
                # Map depreciation based on standard database specs
                dep_map = {
                    "Suzuki Alto": 0.05,
                    "Suzuki Wagon R": 0.04,
                    "Toyota Axio": 0.04,
                    "Honda Vezel": 0.05,
                    "Toyota Prius": 0.06
                }
                scraped_market_data[model_name] = {
                    "base_lkr": round(avg_market_price, 2),
                    "depreciation_per_year": dep_map.get(model_name, 0.05),
                    "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
                }
        except Exception as e:
            print(f"Skipping lookup for {model_name}: {e}")
            
    # Fallback default values if target servers reject requests or time out
    if not scraped_market_data:
        scraped_market_data = {
            "Suzuki Alto": {"base_lkr": 3800000.0, "depreciation_per_year": 0.05, "last_updated": "Fallback Mode"},
            "Suzuki Wagon R": {"base_lkr": 6200000.0, "depreciation_per_year": 0.04, "last_updated": "Fallback Mode"},
            "Toyota Axio": {"base_lkr": 10500000.0, "depreciation_per_year": 0.04, "last_updated": "Fallback Mode"},
            "Honda Vezel": {"base_lkr": 12500000.0, "depreciation_per_year": 0.05, "last_updated": "Fallback Mode"},
            "Toyota Prius": {"base_lkr": 14500000.0, "depreciation_per_year": 0.06, "last_updated": "Fallback Mode"}
        }
        
    with open("market_rates.json", "w") as f:
        json.dump(scraped_market_data, f, indent=4)
        
    return scraped_market_data

if __name__ == "__main__":
    scrape_local_market_prices()