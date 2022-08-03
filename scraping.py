import requests
from bs4 import BeautifulSoup

base_url = "https://www.shopify.co.uk"

html_text = requests.get("https://www.shopify.co.uk/blog").text;
soup = BeautifulSoup(html_text, 'lxml')

articles = soup.find_all('article', class_ = "grid__item grid__item--tablet-up-half article--index")
