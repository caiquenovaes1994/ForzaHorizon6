import requests
from bs4 import BeautifulSoup
import json
import os

URL = 'https://forza.net/fh6cars'
DATA_DIR = 'data'
DATA_FILE = os.path.join(DATA_DIR, 'cars.json')

def scrape_cars():
    print(f"Fetching data from {URL}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return

    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    
    if not table:
        print("Could not find the car table on the page.")
        return

    rows = table.find('tbody').find_all('tr')
    
    scraped_cars = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 4:
            make = cols[0].text.strip()
            car_name = cols[1].text.strip()
            class_pi = cols[3].text.strip()
            
            scraped_cars.append({
                'make': make,
                'car_name': car_name,
                'class_pi': class_pi,
                'adquirido': False,
                'capturado': False
            })

    # Sort alphabetically by Make, then Car Name
    scraped_cars.sort(key=lambda x: (x['make'].lower(), x['car_name'].lower()))

    # Load existing data to preserve checkboxes
    existing_cars = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                for car in data:
                    key = f"{car['make']}_{car['car_name']}"
                    existing_cars[key] = car
            except json.JSONDecodeError:
                print("Error parsing existing JSON. Creating new data.")

    # Merge data
    merged_cars = []
    seen_keys = set()
    for car in scraped_cars:
        key = f"{car['make']}_{car['car_name']}"
        if key in existing_cars:
            car['adquirido'] = existing_cars[key].get('adquirido', False)
            car['capturado'] = existing_cars[key].get('capturado', False)
        merged_cars.append(car)
        seen_keys.add(key)

    # Keep cars that are in the JSON but not on the website
    for key, car in existing_cars.items():
        if key not in seen_keys:
            merged_cars.append(car)

    # Sort again after merging
    merged_cars.sort(key=lambda x: (x['make'].lower(), x['car_name'].lower()))


    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(merged_cars, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully scraped and saved {len(merged_cars)} cars to {DATA_FILE}")

if __name__ == "__main__":
    scrape_cars()
