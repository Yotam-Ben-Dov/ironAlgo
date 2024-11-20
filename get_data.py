# we first need to get data for our classifier
# to do that we'll first connect to each site and extract the html.

import requests
from bs4 import BeautifulSoup

def main():
    headlines = get_headlines("https://www.israelhayom.com/")
    print(headlines)
    
    
def get_headlines(address):
    response = requests.get(address)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = [a.get_text().strip() for a in soup.find_all(class_="jeg_post_title")]
    return headlines

def create_csv():
    pass

if __name__ =="__main__":
    main()