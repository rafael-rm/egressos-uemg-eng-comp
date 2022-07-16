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
buscar_pessoa.send_keys("rafael rodrigues")
buscar_pessoa.send_keys(Keys.ENTER)
time.sleep(delay)
# Iniciar o SOUP
src = navegador.page_source
soup = BeautifulSoup(src, 'lxml')
#### Rodar a pagina para baixo (carregar todos os alunos encontrados)
start = time.time()
# will be used in the while loop
initialScroll = 0
finalScroll = 1000
 
while True:
    navegador.execute_script(f"window.scrollTo({initialScroll}, {finalScroll})")
    # this command scrolls the window starting from
    # the pixel value stored in the initialScroll 
    # variable to the pixel value stored at the
    # finalScroll variable
    initialScroll = finalScroll
    finalScroll += 1000
  
    # we will stop the script for 3 seconds so that 
    # the data can load
    time.sleep(1)
    # You can change it as per your needs and internet speed
  
    end = time.time()
  
    # We will scroll for 20 seconds.
    # You can change it as per your needs and internet speed
    if round(end - start) > 8:
        break
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
for aluno in soup.find_all("div", {'class': 'artdeco-entity-lockup__title ember-view'}):
    print("Nome do aluno: " + aluno.find("div").get_text().strip())
    print("Url do perfil: " + aluno.find("a").get("href"))
    dados = {
        "nome": aluno.find("div").get_text().strip(),
        "url": aluno.find("a").get("href")
    }
    alunos.append(dados)
# Imprimir o dado do primeiro aluno
print("Nome do aluno: " + alunos[0]["nome"])
print("Url do perfil: " + alunos[0]["url"])
#navegador.get(alunos[0]["url"])
navegador.get("https://www.linkedin.com/in/edwaldorodrigues/")
time.sleep(delay)

src = navegador.page_source
soup = BeautifulSoup(src, 'lxml')
graduacao = soup.find_all("div", {'class': 'display-flex flex-row justify-space-between'})
print(graduacao)
