#Imports
import pandas as pd
import unidecode

#Lecture du fichier dans un dataframe pandas
df_communes = pd.read_csv('./Resources/communes-departement-region.csv', sep=',', encoding='utf-8')

#On récupére les colonnes "code_commune_INSEE" et "nom_commune"
df_communes_short = df_communes[['code_commune_INSEE', 'nom_commune', 'code_departement']]
df_communes_short = df_communes_short.rename(columns={'code_commune_INSEE': 'code', 'nom_commune': 'nom', 'code_departement': 'dep'})
df_communes_short['dep'] = df_communes_short['dep'].astype(str)

for index, commune in df_communes_short.iterrows():
    commune['nom'] = commune['nom'].lower()
    commune['nom'] = unidecode.unidecode(commune['nom'])
    commune['nom'] = commune['nom'].replace(' ', '-')
    
    if len(commune['code']) < 5:
        commune['code'] = '0' + commune['code']
        
    if len(commune['dep']) < 3:
        commune['dep'] = '0' + commune['dep']

#Sauvegarde des nouvelles données dans un nouveau csv
df_communes_short.to_csv('./Resources/communes_short.csv', sep=';', encoding='utf-8', index=False)