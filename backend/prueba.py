
import requests  
from bs4 import BeautifulSoup  
    
def getdata(url):  
    r = requests.get(url)  
    return r.text  
lista=[]
htmldata = getdata("https://mashable.com/article/our-flag-means-death-fandom-david-jenkins")  
soup = BeautifulSoup(htmldata, 'html.parser')  

imagen_tag = soup.find('meta', attrs={'property': 'og:image'} or {'name': 'og:image'})
if imagen_tag:
    imagen_url = imagen_tag.get('content')
    print("URL de la imagen encontrada:", imagen_url)
