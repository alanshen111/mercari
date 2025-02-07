import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

previous_listings = []
item_limit = 5

# Fetch and return dictionary of item information
def fetch_listings(query):

    # Get target URL
    url = f"https://jp.mercari.com/en/search?keyword={query}&category_id=1&lang=en&sort=created_time&order=desc"

    print(f'Fetching listings from {url}')
    
    # We use Selenium first to load the page 
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    chrome_install = ChromeDriverManager().install()
    folder = os.path.dirname(chrome_install)
    chromedriver_path = os.path.join(folder, "chromedriver.exe")
    driver = webdriver.Chrome(service=ChromeService(chromedriver_path), options=options)
    driver.get(url)
    try:
        wait = WebDriverWait(driver, 20)
        item_grid = wait.until(EC.presence_of_element_located((By.ID, 'item-grid')))
        page_source = driver.page_source
    except Exception as e:
        print(f"Could not load page: {e}")
        driver.quit()
        return []
    driver.quit()

    # Use BeautifulSoup to get the listing grid
    soup = BeautifulSoup(page_source, 'html.parser')
    listings = []
    item_grid = soup.find('div', {'id': 'item-grid'})
    if not item_grid:
        print("Could not find the item grid")
        return listings

    # Extract item information
    for item in item_grid.select('li[data-testid="item-cell"]')[0:item_limit]: 
        link_tag = item.find('a', {'data-testid': 'thumbnail-link'})
        price_tag = item.find('span', class_='merPrice')
        image_tag = item.find('img', {'loading': 'lazy'})
        
        if link_tag and price_tag:
            link_tag = link_tag['href']
            link = 'https://jp.mercari.com' + link_tag
            price = price_tag.text.strip()
            image = image_tag['src']
            listings.append({
                'price': price,
                'link': link,
                'image': image
            })
            # print(f'Listing: {link}')

    return listings