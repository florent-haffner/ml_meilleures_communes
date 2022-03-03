#Imports
from pydoc import describe
import pandas as pd
from unidecode import unidecode
import numpy as np
from datetime import datetime
from tqdm import tqdm

#Constantes
DATASET_FILE = './Resources/communes-departement-region.csv'
CSV_FILE = './Resources/communes_short.csv'

if __name__ == '__main__':

    tqdm.pandas()

    #Affichage de la date/heure du début de traitement
    now = datetime.now()
    start_time_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(f"Début du traitement des données : {start_time_string}.\n")
    
    #Lecture du fichier dans un dataframe pandas
    print(f"Récupération du fichier '{DATASET_FILE}'.")
    df_communes = pd.read_csv(DATASET_FILE, sep=',', encoding='utf-8')

    #On récupére les colonnes "code_commune_INSEE" et "nom_commune"
    df_communes_short = df_communes[['code_commune_INSEE', 'nom_commune', 'code_departement']]
    df_communes_short = df_communes_short.rename(columns={'code_commune_INSEE': 'code', 'nom_commune': 'nom', 'code_departement': 'dep'})
    df_communes_short['code'] = df_communes_short['code'].astype(str)
    df_communes_short['dep'] = df_communes_short['dep'].astype(str)

    #Suppression des doublons
    df_communes_short = df_communes_short.drop_duplicates(subset=['code'])

    #Création de la colonne index
    df_communes_short['index'] = 0
    df_communes_short['index'] = df_communes_short['index'].astype(int)

    #Alimentation colonne index
    indexes = np.arange(0, df_communes_short.shape[0])
    df_communes_short['index'] = indexes

    #Gestion colonne nom
    print("Gestion de la colonne 'nom' :")
    df_communes_short['nom'] = df_communes_short['nom'].progress_apply(lambda x: unidecode(x.lower()).replace(' ', '-'))
        
    #Gestion colonnes code et dep
    print("\nGestion de la colonne 'code' :")
    df_communes_short['code'] = df_communes_short['code'].progress_apply(lambda x: '0' + x if len(x) < 5 else x)
    print("Gestion de la colonne 'dep' :")
    df_communes_short['dep'] = df_communes_short['dep'].progress_apply(lambda x: '0' + x if len(x) < 2 else x)

    #Réarangement des colonnes => index passe en première position
    cols = df_communes_short.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df_communes_short = df_communes_short[cols]

    #Ajout de la colonne url
    df_communes_short['url'] = ""
    df_communes_short['url'] = df_communes_short['url'].astype(str)
    
    #Sauvegarde des nouvelles données dans un nouveau csv
    df_communes_short.to_csv(CSV_FILE, sep=';', encoding='utf-8', index=False)
    print(f"\nEnregistrement dans le fichier '{CSV_FILE}'.\n")
    
    #Affichage de la date/heure de fin
    now = datetime.now()
    end_time_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(f"Fin du traitement des données : {end_time_string}.\n")