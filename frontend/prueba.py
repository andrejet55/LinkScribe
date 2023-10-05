import requests
from bs4 import BeautifulSoup

URL='https://www.eladerezo.com/cultura/pasta-masterclass-el-2o-libro-de-mateo-zielonka.html'

response = requests.get(URL)
html_content = response.content

soup = BeautifulSoup(html_content, "html.parser")
img_url = soup.find("img")["src"]

img_data = requests.get(img_url).content
        
print(img_data)