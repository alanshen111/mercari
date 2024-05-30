import io
import requests
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import tkinter as tk
from PIL import Image, ImageTk
import webbrowser
import chime

def fetch_listings(search_query=''):
    url = f"https://jp.mercari.com/en/search?keyword=lizlisa&category_id=1&lang=en&sort=created_time&order=desc"
    
    # We use Selenium first to load the page and then pass the source to BeautifulSoup later
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
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

    soup = BeautifulSoup(page_source, 'html.parser')
    listings = []
    item_grid = soup.find('div', {'id': 'item-grid'})
    if not item_grid:
        print("Could not find the item grid.")
        return listings

    for item in item_grid.select('li[data-testid="item-cell"]')[0:5]:  # Only get the first 5 items
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

def check_for_new_listings():

    new_listings = fetch_listings()
    new_items = [item for item in new_listings if item not in previous_listings]
    if new_items:
        chime.info()
        print("New listings found:")
        for item in new_items:
            print(item)
        display_tkinter_ui(root, frame, new_items)
    else:
        print("No new listings.")
    previous_listings.extend(new_items)

def check_listings_periodically():
    while True:
        check_for_new_listings()
        time.sleep(60) 

def display_tkinter_ui(root, frame, listings):

    global full_listings
    full_listings = listings + full_listings

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

def fetch_image(url):
    response = requests.get(url)
    image_data = response.content  
    if not image_data:
        raise Exception(f"Image not found at {url}")
    image = Image.open(io.BytesIO(image_data))
    image = ImageTk.PhotoImage(image)
    return image

chime.theme("pokemon")

root = tk.Tk()
root.title("New Mercari Listings")
root.geometry("600x600")
root.option_add("*Background", "pink")

canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor=tk.NW)

scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.config(yscrollcommand=scrollbar.set)

frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

previous_listings = []
full_listings = []

thread = threading.Thread(target=check_listings_periodically)
thread.daemon = True
thread.start()

root.mainloop()
