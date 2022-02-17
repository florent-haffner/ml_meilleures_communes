#Imports
import pandas as pd

#Lecture du fichier dans un dataframe pandas
df_communes = pd.read_csv('communes-departement-region.csv', sep=',', encoding='utf-8')

#On récupére les colonnes "code_commune_INSEE" et "nom_commune"
df_communes_short = df_communes[['code_commune_INSEE', 'nom_commune']]
df_communes_short = df_communes_short.rename(columns={'code_commune_INSEE': 'code', 'nom_commune': 'nom'})

#Sauvegarde des nouvelles données dans un nouveau csv
df_communes_short.to_csv('./communes_short.csv', sep=';', encoding='utf-8', index=False)