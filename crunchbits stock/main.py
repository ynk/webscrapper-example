#writing a bs4 script to scrape the data from a server hosting website to check if a product is in stock, the store uses WHMCS as their backend
#the script will check the website every 5 minutes and send a webhook to discord if the product is in stock

import requests
import bs4
import time
import json
import os

def time_print(msg,color="green"):
    #print the time
    #could use a better way to do this but it works
    color = color.lower()
    if color == "green":
        print("\033[92m {}\033[00m" .format(time.strftime("%H:%M:%S")), msg)
    elif color == "red":
        print("\033[91m {}\033[00m" .format(time.strftime("%H:%M:%S")), msg)
    elif color == "yellow":
        print("\033[93m {}\033[00m" .format(time.strftime("%H:%M:%S")), msg)
    else:
        print(time.strftime("%H:%M:%S"), msg)





def get_data():
    #get the data from the website
    url = "https://my.crunchbits.com/store/big-storage-vps/2tb-storage-vps"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100102 Firefox/119.0"}, timeout=5)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    return soup


def parse_data(soup):
    #parse the data from the website
    #check if alert alert-danger error-heading exists if not the product is in stock
    if soup.find("div", {"class": "alert alert-danger error-heading"}):
        time_print("Product is out of stock",color="red")
        return False
    else:
        time_print("Product is in stock",color="green")
        return True

def let_me_know():
    #send a webhook to discord
    webhook_url = "use your own discord webhook url"
    data = {
        "content": "Product is in stock"
    }
    result = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        time_print(err,color="yellow")

while True:
    making_soup = parse_data(get_data())
    if not making_soup:
        pass
    else:
        let_me_know()

    time.sleep(300)

