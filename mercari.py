import threading
import time

# Scraping
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Interface
import requests
import tkinter as tk
from PIL import Image, ImageTk
import io
import webbrowser
import chime

# Global variables
root = tk.Tk()
canvas = tk.Canvas(root)
frame = tk.Frame(canvas)
previous_listings = []
full_listings = []

# Fetch and return dictionary of item information
def fetch_listings(search_query):

    # Get target URL
    url = f"https://jp.mercari.com/en/search?keyword={search_query}&category_id=1&lang=en&sort=created_time&order=desc"
    
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
        print(f"An error occurred: {e}")
        driver.quit()
        return []
    driver.quit()

    # Use BeautifulSoup to get the listing grid
    soup = BeautifulSoup(page_source, 'html.parser')
    listings = []
    item_grid = soup.find('div', {'id': 'item-grid'})
    if not item_grid:
        print("Could not find the item grid.")
        return listings

    # Extract item information
    for item in item_grid.select('li[data-testid="item-cell"]')[0:5]:  # Limit to 5 items
        link_tag = item.find('a', {'data-testid': 'thumbnail-link'})
        price_tag = item.find('span', class_='merPrice')
        image_tag = item.find('img', {'loading': 'lazy'})
        
        if link_tag and price_tag:
            link = link_tag['href']
            price = price_tag.text.strip()
            image = image_tag['src']
            listings.append({
                'price': price,
                'link': 'https://jp.mercari.com' + link,
                'image': image
            })

    return listings

# Attempt to fetch new listings and display them
def check_for_new_listings(search_query):

    listings = fetch_listings(search_query)
    new_listings = [item for item in listings if item not in previous_listings]
    if new_listings:
        chime.info()
        print("New listings found:")
        for item in new_listings:
            print(item)
        display_tkinter_ui(new_listings)
    else:
        print("No new listings.")

    previous_listings.extend(new_listings)

# Check for new listings every minute
def check_listings_periodically(search_query):
    while True:
        check_for_new_listings(search_query)
        time.sleep(60)

# Display the listings in a Tkinter window
def display_tkinter_ui(new_listings):

    global full_listings
    full_listings = new_listings + full_listings

    for widget in frame.winfo_children():
        widget.grid_forget()

    for i, listing in enumerate(full_listings):
        listing_frame = tk.Frame(frame)
        listing_frame.grid(row=i, column=0, padx=10, pady=10)

        price_label = tk.Label(listing_frame, text=listing['price'])
        price_label.grid(row=0, column=0)

        image = fetch_image(listing['image'])
        image_label = tk.Label(listing_frame, image=image)
        image_label.image = image
        image_label.grid(row=0, column=1)

        link_label = tk.Label(listing_frame, text=listing['link'], fg="blue", cursor="hand2")
        link_label.bind("<Button-1>", lambda event, link=listing['link']: webbrowser.open(link))
        link_label.grid(row=0, column=2)

    root.update_idletasks() 
    canvas.config(scrollregion=canvas.bbox("all")) 

# Fetch and return image from URL
def fetch_image(url):
    response = requests.get(url)
    image_data = response.content  
    if not image_data:
        raise Exception(f"Image not found at {url}")
    image = Image.open(io.BytesIO(image_data))
    image = ImageTk.PhotoImage(image)
    return image

# Set up the Tkinter window
chime.theme("pokemon")
root.title("New Mercari Listings")
root.geometry("600x600")
root.option_add("*Background", "pink")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
canvas.create_window((0, 0), window=frame, anchor=tk.NW)
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.config(yscrollcommand=scrollbar.set)
frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

# Begin the event loop
thread = threading.Thread(target=check_listings_periodically, args=("lizlisa",))
thread.daemon = True
thread.start()
root.mainloop()
