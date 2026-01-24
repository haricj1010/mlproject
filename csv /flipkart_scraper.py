import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os

# Configuration
BASE_URL = "https://www.flipkart.com/search?q=headphone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

def get_product_data(page_num):
    url = f"{BASE_URL}&page={page_num}"
    print(f"Scraping Page {page_num}...")
    
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page_num}. Status: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Container for products - Multiple fallback options for headphones
        products = soup.find_all('div', class_='jIjQ8S')
        
        # Fallback 1: Different class names
        if not products:
            products = soup.find_all('div', class_='tUxRFH')
        
        # Fallback 2: Look for product cards
        if not products:
            products = soup.find_all('div', class_='yKfEBb')
        
        # Fallback 3: Look for any div with product link structure
        if not products:
            products = soup.find_all('a', class_='k7wcnx')
        
        # Fallback 4: Look for any div containing price
        if not products:
            price_divs = soup.find_all('div', class_='hZ3P6w')
            products = [div.parent for div in price_divs if div.parent]

        if not products:
            print(f"No product containers found on page {page_num}")
            return []

        page_data = []
        
        for product in products:
            try:
                # Name - Multiple selectors for headphones
                name_tag = product.find('div', class_='RG5Slk')
                if not name_tag:
                    name_tag = product.find('div', class_='KzDlHZ')
                if not name_tag:
                    name_tag = product.find('a', class_='wjcEIp')
                if not name_tag:
                    name_tag = product.find('div', class_='VUzEbd')
                name = name_tag.text.strip() if name_tag else "N/A"
                
                # Price - Multiple selectors
                price_tag = product.find('div', class_='hZ3P6w')
                if not price_tag:
                    price_tag = product.find('div', class_='Nx9bqj')
                if not price_tag:
                    price_tag = product.find('div', class_='yQyS8U')
                price = price_tag.text.strip() if price_tag else "N/A"
                
                # Rating
                rating_tag = product.find('div', class_='MKiFS6')
                if not rating_tag:
                    rating_tag = product.find('div', class_='XQDdHH')
                if not rating_tag:
                    rating_tag = product.find('span', class_='Y8H7K4')
                rating = rating_tag.text.strip() if rating_tag else "N/A"
                
                # Reviews & Ratings Count
                stats_container = product.find('span', class_='PvbNMB')
                ratings_count = "0"
                reviews_count = "0"
                
                if stats_container:
                    spans = stats_container.find_all('span')
                    for sp in spans:
                        txt = sp.text.strip()
                        if 'Ratings' in txt:
                            ratings_count = txt.replace('Ratings', '').strip()
                        elif 'Reviews' in txt:
                            reviews_count = txt.replace('Reviews', '').strip()
                
                # Features
                features_list = []
                ul = product.find('ul', class_='HwRTzP')
                if ul:
                    features = ul.find_all('li', class_='DTBslk')
                    features_list = [f.text.strip() for f in features]
                
                feature_str = " | ".join(features_list)
                
                page_data.append({
                    'Product Name': name,
                    'Price': price,
                    'Rating': rating,
                    'Ratings Count': ratings_count,
                    'Reviews Count': reviews_count,
                    'Features': feature_str
                })
                
            except Exception as e:
                print(f"Error parsing product: {e}")
                continue
                
        print(f"Found {len(page_data)} products on page {page_num}")
        return page_data

    except Exception as e:
        print(f"Error retrieving page {page_num}: {e}")
        return []

def main():
    all_data = []
    target_count = 5000  # Increased target for headphones
    current_page = 1
    search_query = "headphone"  # Current search query
    filename = 'flipkart_laptops_full.csv'
    
    # Check if we already have some data and if search query changed
    if os.path.exists(filename):
        try:
            print(f"Found existing data file {filename}. Loading...")
            df = pd.read_csv(filename)
            
            # Check if we need to reset for new search query
            if len(df) > 0:
                # Check if existing data is from different search
                sample_name = str(df.iloc[0]['Product Name']).lower()
                print(f"Sample existing product: {sample_name[:50]}...")
                
                # Force reset if we're looking for headphones but have laptops
                if search_query.lower() in ['headphone', 'headphones'] and ('laptop' in sample_name or 'notebook' in sample_name or 'chromebook' in sample_name):
                    print(f"Detected laptop data but searching for {search_query}. Resetting data...")
                    all_data = []
                    # Remove old file
                    os.remove(filename)
                    print("Old laptop data file removed.")
                elif search_query.lower() in ['laptop', 'laptops'] and ('headphone' in sample_name or 'earphone' in sample_name or 'bluetooth' in sample_name):
                    print(f"Detected headphone data but searching for {search_query}. Resetting data...")
                    all_data = []
                    # Remove old file
                    os.remove(filename)
                    print("Old headphone data file removed.")
                else:
                    all_data = df.to_dict('records')
                    print(f"Loaded {len(all_data)} existing records for {search_query}.")
        except Exception as e:
            print(f"Error loading existing file: {e}")
            
    print(f"Starting scrape for: {search_query}")
    print(f"Target: {target_count} products")
            
    while len(all_data) < target_count:
        data = get_product_data(current_page)
        
        if not data:
            print("No data found on this page. Stopping.")
            break
            
        all_data.extend(data)
        print(f"Collected {len(data)} items. Total: {len(all_data)}")
        
        # Debug: Show first item of each page
        if data and len(data) > 0:
            print(f"Sample item: {data[0]['Product Name'][:50]}...")
        
        # Save updated dataset
        df = pd.DataFrame(all_data)
        df.to_csv(filename, index=False)
        
        current_page += 1
        
        # Respectful delay (increased to avoid 429 rate limits)
        delay = random.uniform(3, 7)  # Reduced delay for faster scraping
        print(f"Waiting {delay:.2f} seconds...")
        time.sleep(delay)
        
        # Safety break
        if current_page > 100:
            print("Reached page limit.")
            break

    print(f"Scraping complete. Total items: {len(all_data)}")
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    main()
