import pandas as pd
import re
#import pywhatkit
from prettytable import PrettyTable
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


########## GET URL ##########
url = 'https://www.livelo.com.br/ganhe-pontos-compre-e-pontue'


######### Initialize the browser #########
options = Options()
options.headless = False  # False allows me to visualize what is happening (opens the browser)
driver = webdriver.Chrome(options=options)  #INITIALIZE BROWSER
driver.get(url)  #GET URL
time.sleep(10)   #GIVE TIME TO LOAD

######### SELECTING WHAT I WANT TO SCRAPE #########
element = driver.find_element_by_xpath("//div[@id='div-cardsParity']")
html_content = element.get_attribute('outerHTML')   #GET HTML
soup = BeautifulSoup(html_content,'html.parser')   #PARSES IT
table = soup.find_all('div', class_='parity__card')   #Wprlomg pm 07/02/2023

names = []
valores = []
for k in range(len(table)):
    names.append(table[k].select('div>div>div>img[alt]')[0]['alt'])
    valor = table[k].select('div>div>div>span')
    aaa = []
    for span in valor:
        (aaa.append(span.get_text()))
    x = " ".join(aaa)
    valores.append(x)

tabela = PrettyTable()
tabela.field_names = ["Loja", "Pontos"]

for i in range(len(names)):
    tabela.add_row([names[i],valores[i]])

print(tabela)


# Threshold value
threshold = 7

# Create a regular expression pattern to match numbers in the strings
pattern = r'\b\d+\b'

# Find all strings with numbers greater than the threshold
result = []
for i, s in enumerate(valores):
    # Find all numbers in the string
    numbers = re.findall(pattern, s)
    # Check if any of the numbers are greater than the threshold
    if any(int(n) > threshold for n in numbers):
        result.append(i)

#print(result)

top_lojas = []
top_pontos = []
for n in result:
    top_lojas.append(names[n])
    top_pontos.append(valores[n])

tabela_dos_top = PrettyTable()
tabela_dos_top.field_names = ["Lojas", "Pontos"]
for i in range(len(top_lojas)):
    tabela_dos_top.add_row([top_lojas[i],top_pontos[i]])

#print(tabela_dos_top)
############ CRIANDO UM DATAFRAME ############
linhas = top_lojas
dados = top_pontos

### melhorando os dados ###
pattern = r'\$'
k = []
for i in dados:
    if len(re.findall(pattern,i))>1:
        k.append(re.findall(r'.\$.+\d',i[-26:])[0])
    else:
        k.append(re.findall(r'.\$.+\d',i)[0])

coluna = ["Pontos"]


df = pd.DataFrame(data=k,index=linhas,columns=coluna)
df_string = df.to_string()
print(df_string)

driver.quit()

# Phone number of the recipient (include the country code)
#josi = "Cellphone number"
#digao = ""

# Current time (hour and minute)
#hour = 10
#minute = 34


# Send the message at the specified time
#pywhatkit.sendwhatmsg(phone_no=digao,message=df_string,time_hour=hour,time_min=minute)
