# -*- coding: utf-8 -*-
"""TPFinal- AndreaR.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/110sptpxgTZKJLNcDaJlG3uYzlltScZDw

# Imports
"""

from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt

"""#Escrapeado"""

total_productos = []
for pag in range(1,6): 
  r = requests.get(f"https://www.superseis.com.py/search.aspx?searchterms=galletita&pageindex={pag}")
  content = r.content
  soup = BeautifulSoup(content)

  productos = soup.find_all("div", attrs = {"class":"item-box"})

  for producto in productos:
    nombre_producto = producto.find("h2", attrs = {"class":"product-title"}).get_text(strip = True)
    precio_producto = producto.find("span", attrs = {"class":"price-label"}).get_text(strip = True)
    
    stopwords = ["de", "con", "sabor"]
    palabras_nombre = nombre_producto.split(sep = " ")
    for palabra in palabras_nombre: 
      if palabra.lower() in stopwords:
        sabor_producto = palabras_nombre[palabras_nombre.index(palabra)+1]
        break
    else:
      sabor_producto = "OTROS"
    
    total_productos.append([nombre_producto, precio_producto, sabor_producto])

df_productos = pd.DataFrame (total_productos, columns= ["Nombre del producto", "Precio del producto", "Sabor del producto"])
df_productos

sabores = []
for sabor in df_productos["Sabor del producto"]:
  if sabor.upper() not in sabores: 
    sabores.append(sabor.upper())
  else: 
    continue

print(sabores)

cantidad_sabor = []
for sabor in sabores: 
  cantidad_sabor.append(list(df_productos["Sabor del producto"]).count(sabor))

print(cantidad_sabor)

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(sabores, cantidad_sabor)
plt.xticks(rotation = "vertical")
plt.show()

df_productos.to_csv("archivo.csv")