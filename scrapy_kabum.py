import requests
from random import randint
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

class KabumSpider:
    
    SCRAPEOPS_API_KEY = os.getenv('API_KEY')
    url_list = [
    'https://www.kabum.com.br/hardware/processadores',
  
        ]
    
    def get_user_agent_list(self):
        response = requests.get('http://headers.scrapeops.io/v1/user-agents?api_key=' + self.SCRAPEOPS_API_KEY)
        json_response = response.json()
        return json_response.get('result', [])

    def get_random_user_agent(self,user_agent_list):
        random_index = randint(0, len(user_agent_list) - 1)
        return user_agent_list[random_index]
    
    def get_urls(self):
        user_agent_list = self.get_user_agent_list()
        for url in self.url_list:
            headers = {'User-Agent': self.get_random_user_agent(user_agent_list)}
            
            response  = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(response.content, 'lxml')
            paginas = soup.find_all("a",class_="page")
            
            pagina = [pagina.get_text()  for pagina in paginas][-1]
            for i in range(int(pagina)+1):
                pagina = f'https://www.kabum.com.br/hardware/processadores?page_number={i}'
                
                response  = requests.get(url=pagina, headers=headers)
                soup = BeautifulSoup(response.content, 'lxml')
                
        
                try:
                    urls = soup.find_all("div", class_="sc-ff8a9791-7 JDtDP productCard")
                    url_produtos = [url.find("a").get("href") for url in urls]
                except Exception as e:
                    print(e)

                try:
                    nomes = soup.find_all("span",class_="sc-d99ca57-0 bzucsr sc-ff8a9791-16 kMfyNu nameCard")
                    nome = [nome.get_text() for nome in nomes if nome !='']
                except Exception as e:
                    print(e)
                
                try:
                    precos = soup.find_all("span",class_="sc-3b515ca1-2 hQOqhY priceCard")
                    preco = [preco.get_text().strip().replace("R$","").replace("\xa0","").replace(".","").replace(",",".") for preco in precos]
                except Exception as e:
                    print(e)

                try:
                    imagens = soup.find_all("img",class_="imageCard")
                    imagem = [imagem['src'] for imagem in imagens]
                except Exception as e:
                    print(e)
                    
                for i in range(len(url_produtos)):
                    try:
                        produtos = {
                            "URL_PRODUTO":'https://www.kabum.com.br' + url_produtos[i],
                            "NOME":nome[i],
                            "PRECO":preco[i],
                            "IMAGEM":imagem[i]}
                        yield produtos
                    except Exception as e:
                        print(e)
            

spyder = KabumSpider()
items = spyder.get_urls()
for item in items:
    print(item)

