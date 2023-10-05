from transformers import pipeline
from bs4 import BeautifulSoup
import requests
import tensorflow as tf


class Scrapper(object):
    
    def __init__(self): 

        self.summarizer = pipeline("summarization",framework='tf')
        

    def read_url(self,url:str):
        
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find_all(['p','h1','h2'])
        text = [result.text for result in results]
        return text

    def text_processor(self,text):

        max_chunk = 500
        ARTICLE = ' '.join(text)

        ARTICLE = ARTICLE.replace('.', '.<eos>')
        ARTICLE = ARTICLE.replace('?', '?<eos>')
        ARTICLE = ARTICLE.replace('!', '!<eos>')

        sentences = ARTICLE.split('<eos>')
        current_chunk = 0 
        chunks = []
        for sentence in sentences:
            if len(chunks) == current_chunk + 1: 
                if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                    chunks[current_chunk].extend(sentence.split(' '))
                else:
                    current_chunk += 1
                    chunks.append(sentence.split(' '))
            else:
                print(current_chunk)
                chunks.append(sentence.split(' '))

        for chunk_id in range(len(chunks)):
            chunks[chunk_id] = ' '.join(chunks[chunk_id])
        
        return chunks
    
    def summarize(self,chunks):
        
        res = self.summarizer(chunks, max_length=100, min_length=30, do_sample=False)
        text=' '.join([summ['summary_text'] for summ in res])
        return text


    def obtener_titulo(self, url: str):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find_all(['h1'])
        titulo = [result.text for result in results]
        return titulo
        
    def obtener_imagen(self, url: str):

        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        imagen_tag = soup.find('meta', attrs={'property': 'og:image'} or {'name': 'og:image'})
        imagen_url = imagen_tag.get('content')
        return imagen_url