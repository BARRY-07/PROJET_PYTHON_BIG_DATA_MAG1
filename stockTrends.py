import urllib.request
import sys
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

#Pour s'assurer qu'on ait 2 arguments (le fichier python et le lien pour les paramètres)
if len(sys.argv) != 2:
    sys.exit('ERROR: This file execution needs an URL path')


url = sys.argv[1]

file = urllib.request.urlopen(url)

Keys = []
Values = []
#Cette liste vide va prendre les parametres necessaires pour telecharger les données
Final_Values = []
for element in file:
    splits = element.decode().split(":")
    Keys.append((splits[0]))
    Values.append((splits[1]))
for i in Values:
    Final_Values.append(i.strip())

data = yf.Ticker(Final_Values[1])
# le mot weekly n'est pas reconnu, donc on le remplace par 1wk pour les données hebdomadaires
if Final_Values[4] == 'weekly':
    Final_Values[4] = '1wk'
#Pour telecharger les donnees
dataDF = data.history(interval=Final_Values[4], start=Final_Values[2], end=Final_Values[3])
#Convertir des timestamps en dates
dataDF.index = pd.to_datetime(dataDF.index)

#Partie Graphique
fig, ax = plt.subplots()
#Courbes d'evolution normarl
ax.plot(dataDF.index, dataDF['Open'], label='Open Price')
ax.plot(dataDF.index, dataDF['Close'], label='Close Price')
#Courbes d'evolution sous forme de points
ax.plot(dataDF.index, dataDF['Low'], color='green', linewidth=1.0, linestyle='dotted', label='Low Price')
ax.plot(dataDF.index, dataDF['High'], color='red', linewidth=1.0, linestyle='dotted', label='High Price')
plt.legend()
plt.title('Stock prices for '+Final_Values[0])
plt.xlabel('Date')
plt.ylabel('Price')

#Rotation des dates
plt.xticks(rotation=90)

#Ajouter le symbole dollar à l'axe des ordonnées

fmt = '{x:.0f}$'
tick = mtick.StrMethodFormatter(fmt)
ax.yaxis.set_major_formatter(tick)

#Pour que l'application python affiche le resultat final
plt.show()