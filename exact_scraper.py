from playwright.sync_api import sync_playwright
import json
import re

def get_exact_sri_lankan_prices(search_model):
    print(f"Launching Headless Extraction Layer for: {search_model}...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        formatted_query = search_model.lower().replace(" ", "-")
        url = f"https://riyasewana.com/search/{formatted_query}"
        
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            try:
                page.wait_for_selector("li.v-card", timeout=5000)
            except:
                pass
            
            listings = page.locator("li.v-card").all()
            extracted_records = []
            
            for item in listings[:10]:
                title_element = item.locator(".v-card-title a")
                title = title_element.inner_text() if title_element.count() > 0 else "Unknown Asset"
                
                price_element = item.locator(".v-card-price")
                raw_price = price_element.inner_text() if price_element.count() > 0 else "Rs. 0"
                
                clean_price = int(re.sub(r'[^\d]', '', raw_price)) if re.sub(r'[^\d]', '', raw_price) else 0
                
                if clean_price > 0:
                    extracted_records.append({
                        "listing_title": title,
                        "exact_price_lkr": clean_price,
                        "display_price": raw_price
                    })

            
            browser.close()
            return extracted_records

        except Exception as e:
            print(f"Error navigating to market source: {e}")
            browser.close()
            return []

if __name__ == "__main__":
    results = get_exact_sri_lankan_prices("Wagon R")
    print(json.dumps(results, indent=4))