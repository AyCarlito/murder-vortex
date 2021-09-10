import requests
from bs4 import BeautifulSoup
import csv


BASE_URL = "https://en.wikipedia.org"
ALL_KILLERS_URL = "https://en.m.wikipedia.org/wiki/List_of_serial_killers_by_country"

def scrape_killer_list(url, id1, killer_type):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    section = soup.find("section", id=id1)
    lis = section.find_all("li")
    killers = [str(li.find('a')['href']) for li in lis if str(li.find('a')['href']).startswith("/wiki/")]
    individuals = section.find_all("div", {"class": "hatnote"})
    for individual in individuals:
        curr = individual.find('a')['href']
        if (str(curr).startswith("/wiki/List")):
            killers+=scrape_single_country(BASE_URL + curr, killer_type)

    create_file(killer_type, killers)
    return
    
def scrape_single_country(url, killer_type):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table", {'class':"wikitable"})
    
    if(killer_type == "identified") and (soup.find("span", id="Unidentified_serial_killers") is not None):
        tables = tables[0:-1]
    elif(killer_type == "unidentified") and (soup.find("span", id="Unidentified_serial_killers") is not None):
        tables = tables[::-1]
        tables = tables[0:1]
    elif(killer_type == "unidentified") and (soup.find("span", id="Unidentified_serial_killers") is None):
        return []
    
    
    links = []
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            try:
                links.append(row.find('a')['href'])
            except TypeError as e:
                pass
        return links

def create_file(filename, killer_urls):
    with open("data/" + filename + "_killers.csv", "w") as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerow(killer_urls)
        f.close()
    return


def main():
    scrape_killer_list(ALL_KILLERS_URL, "mf-section-1", "identified")
    scrape_killer_list(ALL_KILLERS_URL, "mf-section-2", "unidentified")

if __name__ == "__main__":
    main()


