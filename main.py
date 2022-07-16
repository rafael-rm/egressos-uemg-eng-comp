#### Bibliotecas
from gettext import find
import time
import os
import dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
#### Inicializar variáveis
dotenv.load_dotenv(dotenv.find_dotenv())
usuario = os.getenv("user")
senha = os.getenv("password")

delay = 3
navegador = webdriver.Chrome("chromedriver.exe")
#### Login 
navegador.get("https://www.linkedin.com/login/pt")
time.sleep(delay)

# ID do campo de usuário
usuario_id = navegador.find_element(By.ID, "username")  

# Login do usuário
usuario_id.send_keys(usuario)      

# ID do campo de senha
senha_id = navegador.find_element(By.ID, "password")      

# Senha do usuário
senha_id.send_keys(senha)           

# Clicar no botão de login (submit button)
navegador.find_element(By.XPATH, "//button[@type='submit']").click()
# Abrir a pagina da UEMG na parte de ex-alunos
navegador.get("https://www.linkedin.com/school/uemg/people/")
time.sleep(delay)

# Clicar no botão de busca (search button) e digitar o nome do aluno
buscar_pessoa = navegador.find_element(By.ID, "people-search-keywords")
buscar_pessoa.send_keys("engenharia da computação")
buscar_pessoa.send_keys(Keys.ENTER)
time.sleep(delay)
#### Rodar a pagina para baixo (carregar todos os alunos encontrados)
start = time.time()
initialScroll = 0
finalScroll = 1000
 
while True:
    navegador.execute_script(f"window.scrollTo({initialScroll}, {finalScroll})")

    initialScroll = finalScroll
    finalScroll += 1000
    
    # Mudar conforme a velocidade da internet
    time.sleep(1)
  
    end = time.time()
    
    # Tempo de execução
    if round(end - start) > 60:
        break
# Iniciar o SOUP
src = navegador.page_source
soup = BeautifulSoup(src, 'lxml')
# Pegar a classe que contem o numero de alunos encontrados na pesquisa atual
intro = soup.find("span", {'class': 't-20 t-black t-bold'})

# Remover as palavras do texto encontrado ("X ex-estudantes")
alunos_encontrados = ""
for c in intro.text:
    if c.isdigit():
        alunos_encontrados = alunos_encontrados + c

print("Ex-alunos encontrados: " + alunos_encontrados)
time.sleep(delay)
#### Pegar o nome e URL do perfil de cada aluno encontrado
# Pegar a classe html dos ex-alunos 1 por 1
alunos = []
count = 0
for aluno in soup.find_all("div", {'class': 'artdeco-entity-lockup__title ember-view'}):
    if(count == 1):
        print("Nome do aluno: " + aluno.find("div").get_text().strip())
        print("Url do perfil: " + aluno.find("a").get("href"))
        dados = {
            "nome": aluno.find("div").get_text().strip(),
            "url": aluno.find("a").get("href")
        }
        alunos.append(dados)
    count = 1
import json

# Serializing json
json_object = json.dumps(alunos, indent=4)
 
# Writing to sample.json
with open("data.json", "w") as outfile:
    outfile.write(json_object)
#navegador.get(alunos[0]["url"])
navegador.get("https://www.linkedin.com/in/edwaldorodrigues/")
time.sleep(delay)

src = navegador.page_source
soup = BeautifulSoup(src, 'lxml')
graduacao = soup.find_all("div", {'class': 'display-flex flex-row justify-space-between'})
print(graduacao)
