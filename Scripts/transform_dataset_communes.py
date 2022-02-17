#Imports
import pandas as pd
from unidecode import unidecode
import numpy as np

#Lecture du fichier dans un dataframe pandas
df_communes = pd.read_csv('./Resources/communes-departement-region.csv', sep=',', encoding='utf-8')

#On récupére les colonnes "code_commune_INSEE" et "nom_commune"
df_communes_short = df_communes[['code_commune_INSEE', 'nom_commune', 'code_departement']]
df_communes_short = df_communes_short.rename(columns={'code_commune_INSEE': 'code', 'nom_commune': 'nom', 'code_departement': 'dep'})
df_communes_short['code'] = df_communes_short['code'].astype(str)
df_communes_short['dep'] = df_communes_short['dep'].astype(str)

#Création de la colonne index
df_communes_short['index'] = 0
df_communes_short['index'] = df_communes_short['index'].astype(int)

#Alimentation colonne index
indexes = np.arange(0, df_communes_short.shape[0])
df_communes_short['index'] = indexes

#Gestion colonne nom
df_communes_short['nom'] = df_communes_short['nom'].str.lower()
df_communes_short['nom'] = df_communes_short['nom'].apply(unidecode)
df_communes_short['nom'] = df_communes_short['nom'].str.replace(' ', '-')
    
#Gestion colonnes code et dep
df_communes_short['code'] = df_communes_short['code'].apply(lambda x: '0' + x if len(x) < 5 else x)
df_communes_short['dep'] = df_communes_short['dep'].apply(lambda x: '0' + x if len(x) < 3 else x)

#Réarangement des colonnes => index passe en première position
cols = df_communes_short.columns.tolist()
cols = cols[-1:] + cols[:-1]
df_communes_short = df_communes_short[cols]

#Ajout de la colonne url
df_communes_short['url'] = ""
df_communes_short['url'] = df_communes_short['url'].astype(str)

#Sauvegarde des nouvelles données dans un nouveau csv
df_communes_short.to_csv('./Resources/communes_short.csv', sep=';', encoding='utf-8', index=False)