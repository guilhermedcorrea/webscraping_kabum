# webscraping_kabum
Exemplo simples de um webscraping do site Kabum usando Fake User agents



##Execução do projeto
<br>criar venv: py -3 -m venv venv<br/>
<br>ativar: venv\Scripts\activate<br/>
<br>instalar dependencias: pip freeze > requirements.txt<br/>



```Python
    
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

```

<br>Inicializa a API responsavel pelo Fak eUser agente que fica alternando de forma dinamica.<br/>


```Python
    
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


```

<br>Faz o parser, obtem as urls das paginas e extrai as informações de cada uma delas.<br/>