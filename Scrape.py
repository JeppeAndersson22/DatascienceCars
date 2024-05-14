import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

######################
####### SCRAPE #######
######################

# List to store DataFrames for each model
data_frames = []

# Dictionary of brands and their corresponding models
brands_and_models = {
    "VW": ["Tiguan", "Touran", "Golf", "Passat", "Polo", "Arteon", "Atlas", "Beetle", "Jetta", "ID. Buzz", "Touareg", "Sharan", "T-Cross", "T-Roc"],
    "Toyota": ["4Runner", "Avalon", "Camry", "Corolla", "Highlander", "Land Cruiser", "Prius", "RAV4", "Supra", "Yaris"],
    "Audi": ["A1", "A3", "A4", "A5", "A6", "A7", "A8", "Q2", "Q3", "Q5", "Q7", "Q8", "TT", "R8"],
    "Mercedes": ["A-Class", "B-Class", "C-Class", "E-Class", "S-Class", "G-Class", "GLA", "GLC", "GLE", "GLS", "CLA", "CL", "SLK", "AMG GT"],
    "Ford": ["Fiesta", "Focus", "Fusion", "Mustang", "Explorer", "Edge", "Escape", "Expedition", "F-150", "Transit"],
    "Renault": ["Clio", "Megane", "Scenic", "Laguna", "Espace", "Kangoo", "Twingo", "Zoe", "Captur", "Kadjar"],
    "Peugeot": ["208", "308", "508", "2008", "3008", "5008", "Partner", "Expert", "Boxer", "Rifter"],
    "BMW": ["1 Series", "2 Series", "3 Series", "4 Series", "5 Series", "6 Series", "7 Series", "X1", "X3", "X5", "Z4", "M2", "M4", "i3"],
    "Opel": ["Corsa", "Astra", "Insignia", "Zafira", "Meriva", "Adam", "Crossland X", "Grandland X", "Mokka", "Vivaro"],
    "Skoda": ["Fabia", "Rapid", "Octavia", "Superb", "Kodiaq", "Karoq", "Scala", "Kamiq", "Yeti", "Citigo"]
}

def scrape_car_info(soup, url, x, model, brand, df):
    """
    Scrape car information from the webpage and store it in a DataFrame.

    Args:
        soup (BeautifulSoup): Parsed HTML content of the webpage.
        url (str): URL of the webpage.
        x (int): Index of the DataFrame to store the scraped information.
        model (str): Car model.
        brand (str): Car brand.
        df (DataFrame): DataFrame to store the scraped information.

    Returns:
        DataFrame: Updated DataFrame with the scraped information.
    """
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
    return df

def scrape_car_price(soup, url, y, df):
    """
    Scrape car prices from the webpage and store them in a DataFrame.

    Args:
        soup (BeautifulSoup): Parsed HTML content of the webpage.
        url (str): URL of the webpage.
        y (int): Index of the DataFrame to store the scraped prices.
        df (DataFrame): DataFrame to store the scraped prices.

    Returns:
        None
    """
    div_elements_price = soup.find_all('div', class_='listing-item-price')
    for div_price in div_elements_price:
        price_content = div_price.next.get_text(strip=True)
        df.loc[y, 'Pris'] = price_content
        y += 1

def scrape_car_header(soup, url, z, df):
    """
    Scrape car headers from the webpage and store them in a DataFrame.

    Args:
        soup (BeautifulSoup): Parsed HTML content of the webpage.
        url (str): URL of the webpage.
        z (int): Index of the DataFrame to store the scraped headers.
        df (DataFrame): DataFrame to store the scraped headers.

    Returns:
        None
    """
    div_elements_header = soup.find_all('div', class_='listing-item-header')
    for div_header in div_elements_header:
        p_tag = div_header.find('p', class_='truncated')
        dealer_content = p_tag.get_text(strip=True)
        df.loc[z, 'Sælger'] = dealer_content
        z += 1
    div_elements_daysforsale = soup.find_all('div', class_="price-history")
    z = 0
    for div_daysforsale in div_elements_daysforsale:
        daysforsale_content = div_daysforsale.get_text(strip=True)
        df.loc[z, 'DageTilSalg'] = daysforsale_content
        z += 1

def has_listings(soup):
    """
    Check if the webpage contains car listings.

    Args:
        soup (BeautifulSoup): Parsed HTML content of the webpage.

    Returns:
        bool: True if the webpage contains listings, False otherwise.
    """
    no_results_message = soup.find('div', class_='no-search-results')
    return no_results_message is None

def scrapeCars():
    """
    Scrape car information.

    Returns:
        DataFrame: DataFrame containing the scraped car information.
    """
    for brand, models in brands_and_models.items():
        for model in models:
            x = 0
            y = 0
            z = 0
            page_number = 1
            base_url = f"https://www.autouncle.dk/da/brugte-biler/{brand}/{model}?page="
            while True:
                url = base_url + str(page_number)
                response = requests.get(url, timeout=60)
                print(f"URL: {url}, Response Status Code: {response.status_code}")
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    if has_listings(soup):
                        df = pd.DataFrame(columns=['Mærke', 'Model', 'Sælger', 'DageTilSalg', 'Årstal', 'Kilometertal', 'Motor', 'Gear', 'Hestekræfter', 'Km/L', 'Co2', 'Pris'])
                        scrape_car_info(soup, url, x, model, brand, df)
                        scrape_car_price(soup, url, y, df)
                        scrape_car_header(soup, url, z, df)
                        data_frames.append(df.copy())
                        page_number += 1
                    else:
                        break
                else:
                    break
                time.sleep(5)
        time.sleep(5)
        result_df = pd.concat(data_frames, ignore_index=True)
    return result_df

### TIL EXCEL ###

def save_to_excel(df, file_path):
    """
    Save the DataFrame to an Excel file.

    Args:
        df (DataFrame): DataFrame to be saved.
        file_path (str): File path of the Excel file.

    Returns:
        None
    """
    df.to_excel(file_path, index=False)
    print(f"Excel file saved to: {file_path}")

# Specify the file name and location on the desktop
file_name = "dirty_car_data.xlsx"
current_directory = os.getcwd()
path = current_directory
file_path = os.path.join(path, file_name)

# Save the DataFrame to an Excel file
dirtyData = scrapeCars()
save_to_excel(dirtyData, file_path)