from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from time import sleep

df = pd.DataFrame(columns=["habitaciones","baños","a_construida","a_total","estacionamientos","precio", "comuna"])
df = None
# URL de la página a scrapeear
url = "https://chilepropiedades.cl/propiedades/venta/casa/region-metropolitana-de-santiago-rm/0"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
# Realiza la solicitud HTTP a la página
response = requests.get(url, headers=headers)
# Verifica que la solicitud fue exitosa (código 200)
for i in range(29,61):
    # Parsear el contenido HTML de la página
    url = f"https://chilepropiedades.cl/propiedades/venta/casa/region-metropolitana-de-santiago-rm/{i}"
    print(url)
    response = requests.get(url, headers=headers)
    print("Response: ",response)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)
    # Encuentra todos los elementos de tipo título de artículos (suponiendo que están en etiquetas <h2>)
    titles = soup.find_all('div', {"class": "clp-premium-table-item"})
    # Imprime cada título
    # print(titles[0])
    tipos={"1":1,"2":949,"3":37960} # CLP, USD, UF

    for titulo in titles:
        fila = {"Estacionamientos:": np.nan, "Baños:":np.nan, "Superficie Construida:":np.nan, "Estacionamientos:": np.nan,"valor" : np.nan, "comuna":np.nan}
        for a in titulo.find_all('span',{"class":"clp-feature-value"}):
            if len(a.parent.find_all('span',{"class": "clp-feature-description"})) != 0:
                label = a.parent.find_all('span',{"class": "clp-feature-description"})[0].text
            print(label, a.text)
            if "m" in a.text:
                try:
                    if fila[label] != np.nan:
                        label = label+"_2"
                    fila[label]=(float(a.text[:-2].replace(",",".")))
                except:
                    fila[label]=np.nan
            else:
                fila[label]=(a.text)


        tipo = (titulo.find_all('span', {"class":"clp-value-container"}))[1]["valueunit"]
        valor = titulo.find_all('span',{"class":"clp-value-container"})[1]["value"]
        if "E" in valor:
            valor = float(valor.split("E")[0])*10**float(valor.split("E")[1])
        else:
            valor = float (valor)
        fila["valor"] = (valor*tipos[tipo])


        fila["comuna"] = ((titulo.find_all('h3',{"class":"sub-codigo-data"}))[0].text.split("/")[2].strip())

        print(fila)
        if df is None:
            df = pd.DataFrame(columns=fila.keys())
        df = pd.concat([pd.DataFrame(fila, index=[0]),df], ignore_index=True)
        print(df)
        #sleep(.5)

df.to_csv("datos2.csv",index=False)
