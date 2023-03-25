import time

import requests as subhandle
import bs4
import cloudscraper


import json

requests = cloudscraper.create_scraper()


#Not that great but serves a nice POC of how it was done

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}


def report_to_discord(msg,endpoint=0):
    if endpoint==0:
        data = {"content": f"<@endpoint1>: {msg}"}
        url = "endpoint1"
    else:
        data = {"content": f"<@discordId2>: {msg}"}
        url = "endpoint2"
    #


    result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})




def check1():
    url = "https://www.awd-it.co.uk/catalogsearch/result/?q=asus+4090"

    found = 0
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            soup = bs4.BeautifulSoup(r.text, "html.parser")
            titles = soup.find_all("div", {"class": "product details product-item-details"})
            for title in titles:
                if title.find("button", {"class": "stock comingsoon"}) or title.find("button", {"class": "stock unavailable"}):
                    print("out of stock")

                else:
                    found+=1

        msg = (f"[{url}] [status code:({r.status_code})] has stock: {found}, checked: {len(titles)}")

        if found != 0:
            print(msg)
            report_to_discord(msg)
        else:
            print(msg)
    except Exception as e:
        report_to_discord(f"[Store1:] {e} on {url}",endpoint=1)
        return


def check2():
    # url = "https://www.box.co.uk/products/ex/true/keywords/13900k"
    # url = "https://www.box.co.uk/products/ex/true/keywords/30000"
    url = "https://www.box.co.uk/products/ex/true/keywords/asus+4090"
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        report_to_discord(f"Failed url: {url} status code: {r.status_code}",endpoint=1)
        return

    soup = bs4.BeautifulSoup(r.text, "html.parser")
    # get all tags with class p-list-title-wrapper
    titles = soup.find_all("div", {"class": "product-list-item"})
    found = 0
    pre_order = 0
    # check if theres a buy button
    for title in titles:
        # check if btn green small pq-add p-list-add-btn pq-track-event exists
        if title.find("a", {"class": "btn green small pq-add p-list-add-btn pq-track-event"}):
            found += 1
        elif title.find("a", {"class": "btn green small"}):
            print("pre order found")
            found += 1
            pre_order += 1
            # report_to_discord("Pre order found")

    msg = (f"[{url}] [status code:({r.status_code})] has stock: {found}, pre order: {pre_order}, checked: {len(titles)}")
    if found != 0:
        print(msg)
        report_to_discord(msg)
    else:
        print(msg)


def check3():
    url = "https://www.scan.co.uk/search?q=asus+16384+Core"
    # url = "https://www.scan.co.uk/search?q=i9"
    #url = "https://www.scan.co.uk/search?q=asus+4090"
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        report_to_discord(f"Failed url: {url} status code: {r.status_code}",endpoint=1)
        return
    soup = bs4.BeautifulSoup(r.text, "html.parser")

    # check for all productColumns
    titles = soup.find_all("li", {"class": "product"})
    found = 0

    #print("products:", len(titles))
    for title in titles:
        # check if btn exists

        if title.find("a", {"class": "btn"}):
            found += 1
            # report_to_discord(f"{url} has stock")
        else:
            pass
            # print("button not found")

    msg = (f"[{url}] [status code:({r.status_code})] has stock: {found}, checked: {len(titles)}")
    if found != 0:
        print(msg)
        report_to_discord(msg)
    else:
        print(msg)

def check4():
    url = "https://www.pcspecialist.co.uk/computers/intel-z790-ddr5-pc/"
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        report_to_discord(f"Failed url: {url} status code: {r.status_code}",endpoint=1)
        return
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    #check the entire page for an option with the word 4090 in

    products = soup.find_all(lambda tag:tag.name=="option" and "4090" in tag.text)
    # check if x length is greater than one
    found = 0
    if len(products) > 1:
        for item in products:
            print(item.text)
            found+=1

    msg = (f"[{url}] [status code:({r.status_code})] has stock: {found}")

    if found != 0:
        print(msg)
        report_to_discord(msg)
    else:
        print(msg)



if __name__ == "__main__":
    runs = 0
    while True:
        runs+=1
        print(f"Run: {runs}")
        #check1()
        try:
            check1()
        except Exception as e:
            report_to_discord(f"Error: {e}",endpoint=1)
        try:
            check2()
        except Exception as e:
            report_to_discord(f"Error: {e}",endpoint=1)
        try:
            check3()
        except Exception as e:
            report_to_discord(f"Error: {e}",endpoint=1)
        try:
            check4()
        except Exception as e:
            report_to_discord(f"Error: {e}",endpoint=1)

        print("Completed run going to sleep")

        time.sleep(180)

