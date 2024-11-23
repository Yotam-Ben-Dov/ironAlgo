import re
import csv
import requests
from bs4 import BeautifulSoup

def get_data(sources):
    headlines = [hl for s in sources for hl in get_headlines(s)]
    create_csv(headlines)
    
def get_headlines(address):
    # get the html file
    response = requests.get(address)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []
    # separate into cases between haaretz and israel hayom due to different site programming
    # convert it to list of dicts for ease of writing
    if "haaretz" in address:
        # get the headlines
        articles = [a for a in soup.find_all("article")]
        headlines = [a.contents[0].get_text().strip() for a in articles] # filter them for headlines
        # remove timestamps with regex
        headlines = [' '.join(a.split(' ')[2:]) if re.search("^(\d:\d\d|\d\d:\d\d) [APM]{2}", a) else a for a in headlines]
        headlines = [{"headline": a, "magazine": "haaretz"} for a in headlines if len(a) > 2]
        
    elif "israelhayom" in address:
        # get headlines
        headlines = [a.get_text().strip() for a in soup.find_all(class_="jeg_post_title")]
        headlines = [{"headline": a, "magazine": "israel hayom"} for a in headlines if len(a) > 2]
    
    return headlines

def create_csv(headlines): # creates a csv file of the headlines and their tag
    with open('headlines.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["headline", "magazine"])
        writer.writeheader()
        writer.writerows(headlines)
