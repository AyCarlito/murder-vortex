from os import link
from sre_constants import error
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random


def make_clickable(val):
    name, url = val.split('#')
    return f'<a href="{url}">{name}</a>'

def create_table(url):
    base_url = "https://en.wikipedia.org"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {'class':"wikitable"})
    rows = table.find_all('tr')

    links = []
    for row in rows:
        try:
            links.append(base_url + row.find('a')['href'])
        except TypeError as e:
            pass
    
    df = pd.read_html(str(table))[0].drop(["Source"], axis=1)
    df['Links'] = links
    df['Name'] = df['Name'] + '#' + df['Links']
    df({'Name': make_clickable})
    with open("identified_killers_table.html", "w") as f:
        f.write(df.to_html(escape=False))
        f.close()
    return

def scrape_killer(url):
    base_url = "https://en.wikipedia.org"
    response = requests.get(base_url + url)
    soup = BeautifulSoup(response.text, "html.parser")
    summary_table = soup.find("table", {'class':"infobox"})
    try:
        mugshot = soup.find("a", {"class": "image"})
    except AttributeError as e:
        pass
    mugshot_url = mugshot.find("img")['src']




def main():

    scrape_killer(create_table("https://en.wikipedia.org/wiki/List_of_serial_killers_in_the_United_States"))

if __name__ == "__main__":
    main()


#df = pd.read_csv("../data/identified_killers.csv")

