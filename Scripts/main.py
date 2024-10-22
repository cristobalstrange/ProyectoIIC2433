from bs4 import BeautifulSoup
import requests
import pandas as pd

df = pd.DataFrame(columns=["habitaciones","baños","a_construida","a_total","estacionamientos","precio", "comuna"])

# URL de la página a scrapeear
url = "https://chilepropiedades.cl/propiedades/venta/casa/region-metropolitana-de-santiago-rm/0"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
# Realiza la solicitud HTTP a la página
response = requests.get(url, headers=headers)
# Verifica que la solicitud fue exitosa (código 200)
for i in range(1109):
    if response.status_code != 200:
        0/0
    # Parsear el contenido HTML de la página
    url = f"https://chilepropiedades.cl/propiedades/venta/casa/region-metropolitana-de-santiago-rm/{i}"
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Encuentra todos los elementos de tipo título de artículos (suponiendo que están en etiquetas <h2>)
    titles = soup.find_all('div', {"class": "clp-premium-table-item"})
    # Imprime cada título
    # print(titles[0])
    tipos={"1":1,"2":949,"3":37960} # CLP, USD, UF
    for titulo in titles:
        fila = []
        for a in titulo.find_all('span',{"class":"clp-feature-value"}):
            # print(a.parent.find_all('span',{"class": "clp-feature-description"})[0].text, a.text)
            if "m" in a.text:
                fila.append(float(a.text[:-2].replace(",",".")))
            else:
                fila.append(a.text)

        tipo = (titulo.find_all('span', {"class":"clp-value-container"}))[1]["valueunit"]
        valor = titulo.find_all('span',{"class":"clp-value-container"})[1]["value"]
        if "E" in valor:
            valor = float(valor.split("E")[0])*10**float(valor.split("E")[1])
        else:
            valor = float (valor)
        fila.append(valor*tipos[tipo])


        fila.append((titulo.find_all('h3',{"class":"sub-codigo-data"}))[0].text.split("/")[2].strip())
        if len(fila) == 6:
            fila.append("nan")
        elif len(fila) <6:
            print(fila)
            0/0
        print(fila)
        df = pd.concat([pd.DataFrame([fila], columns=df.columns), df], ignore_index=True)
        print(df)
else:
    print(f"Error al acceder a la página, código de estado: {response.status_code}")

df.to_csv("datos.csv",index=False)
