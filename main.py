import time
import os
import dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Carrega o arquivo .env com as variáveis de ambiente
dotenv.load_dotenv(dotenv.find_dotenv())
usuario = os.getenv("user")
senha = os.getenv("password")

# Delay para carregar as paginas
delay = 3

# Criar o driver do navegador
driver = webdriver.Chrome("chromedriver.exe")

# Abrir o site
driver.get("https://www.linkedin.com/login/pt")
time.sleep(delay)

# ID do campo de usuário
usuario_id = driver.find_element(By.ID, "username")  

# Login do usuário
usuario_id.send_keys(usuario)      

# ID do campo de senha
senha_id = driver.find_element(By.ID, "password")      

# Senha do usuário
senha_id.send_keys(senha)              

# Clicar no botão de login (submit button)
driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(delay)

# Abrir a pagina da UEMG na parte de ex-alunos
driver.get("https://www.linkedin.com/school/uemg/people/")
time.sleep(delay)

# Clicar no botão de busca (search button) e digitar o nome do aluno
buscar_pessoa = driver.find_element(By.ID, "people-search-keywords")
buscar_pessoa.send_keys("rafael rodrigues")
buscar_pessoa.send_keys(Keys.ENTER)
time.sleep(delay)

# Iniciar o SOUP
src = driver.page_source
soup = BeautifulSoup(src, 'lxml')

# Pegar a classe que contem o numero de alunos encontrados na pesquisa atual
intro = soup.find("span", {'class': 't-20 t-black t-bold'})

# Remover as palavras do texto encontrado ("X ex-estudantes")
alunos_encontrados = ""
for c in intro.text:
    if c.isdigit():
        alunos_encontrados = alunos_encontrados + c

print("Ex-alunos encontrados: " + alunos_encontrados)

intro = soup.find("ul", {'class': 'display-flex list-style-none flex-wrap'})
print(intro)

os.system("pause")