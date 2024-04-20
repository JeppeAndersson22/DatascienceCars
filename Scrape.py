import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from fake_useragent import UserAgent
import os


######################
####### SCRAPE #######
######################

# Initialize UserAgent object
ua = UserAgent()

# List to store DataFrames for each model
data_frames = []

brands_and_models = {
    "VW": ["Tiguan"]
}

'''
brands_and_models = {
    "VW": ["Tiguan", "Touran"],
    "Audi": ["A1","A2","A3", "A4", "A5", "A6"],
    "Ford": ["Fusion", "Focus", "Escape"],
    # Add more brands and models as needed
}
'''
def scrape_car_info(url, x, model, brand):
    headers = {'User-Agent': ua.random}
    div_elements_left = soup.find_all('div', class_='listing-item-info-left')
    j = 4
    for div_left in div_elements_left:
        div_elements_chip = div_left.find_all('div', class_='listing-item-info-chip')
        for div_chip in div_elements_chip:
            text_content = div_chip.get_text(strip=True)
            df.loc[x, df.columns[j]] = text_content
            df.loc[x, 'Model'] = model
            df.loc[x, 'Mærke'] = brand
            j += 1
        x += 1
        j = 4

def scrape_car_price(url, y, model):
    headers = {'User-Agent': ua.random}
    div_elements_price = soup.find_all('div', class_='listing-item-price')
    for div_price in div_elements_price:
        price_content = div_price.next.get_text(strip=True)
        df.loc[y, 'Pris'] = price_content
        y += 1


def scrape_car_header(url, z, model):
    headers = {'User-Agent': ua.random}
    div_elements_header = soup.find_all('div', class_='listing-item-header')
    for div_header in div_elements_header:
        p_tag = div_header.find('p', class_='truncated')
        dealer_content = p_tag.get_text(strip=True)
        df.loc[z, 'Sælger'] = dealer_content
        z += 1
    div_elements_daysforsale = soup.find_all('div', class_="price-history" )
    z = 0     
    for div_daysforsale in div_elements_daysforsale:
        daysforsale_content = div_daysforsale.get_text(strip=True)
        df.loc[z, 'DageTilSalg'] = daysforsale_content
        z += 1

def has_listings(soup):
    """Check if the page contains listings."""
    no_results_message = soup.find('div', class_='no-search-results')
    return no_results_message is None


for brand, models in brands_and_models.items():

    for model in models:
        df = pd.DataFrame(columns=['Mærke','Model', 'Sælger','DageTilSalg', 'Årstal', 'Kilometertal', 'Motor', 'Gear', 'Hestekræfter', 'Km/L', 'Co2', 'Pris'])
        x = 0
        y = 0
        z = 0
        page_number = 1
        base_url = f"https://www.autouncle.dk/da/brugte-biler/{brand}/{model}?page="
        while True:
            url = base_url + str(page_number)
            response = requests.get(url)
            #print(f"URL: {url}, Response Status Code: {response.status_code}")
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                if has_listings(soup):
                    scrape_car_info(url, x, model, brand)
                    scrape_car_price(url, y, model)
                    scrape_car_header(url, z, model)
                    print(df)
                    data_frames.append(df.copy()) 
                    page_number += 1
                    
                else:
                    break
            else:
                break
            #time.sleep(10)
    #time.sleep(100)

# Concatenate all DataFrames in the list into a single DataFrame
result_df = pd.concat(data_frames, ignore_index=True)
print (result_df)

'''
# Specify the file name and location on the desktop
file_name = "car_data.xlsx"
desktop_path = "/Users/jeppeandersson/Desktop"
file_path = os.path.join(desktop_path, file_name)

# Save the DataFrame to an Excel file
result_df.to_excel(file_path, index=False)
print(f"Excel file saved to: {file_path}")
'''

