#Imports
import pandas as pd
import tqdm
import urllib.request
import time
import datetime
import concurrent.futures
# from random import randint
# from time import sleep
import Utils.csv_utils as csv_utils

#Constantes
DATASET_FILE = './Resources/communes_short.csv'
CSV_FILE = './Resources/communes_url.csv'
NROWS = 2000 #Nombre de lignes récupérée dans le dataframe

def get_url(nom, dep, code):    
    url = f"https://www.bien-dans-ma-ville.fr/{nom}-{dep}-{code}"
    try:
        fp = urllib.request.urlopen(url)
        fp.close()
        last_code = code
        #sleep(randint(1,5)) #Permet d'éviter le ban ip du site (Côté négatif, rallonge le temps de traitement)
        return url
    except urllib.error.HTTPError as exception: #On gère l'erreur 404 et on ne fait rien
        pass

if __name__ == '__main__':    
    #On récupère le dernier index   
    last_index = csv_utils.get_last_index(CSV_FILE)
    
    #Récupération du dataframe
    if NROWS != 0: #S'il y a une valeur précise de lignes à récupérer, on récupère ce nombre de colonnes
        df_communes = pd.read_csv(DATASET_FILE, sep=';', encoding='utf-8', dtype=str, skiprows=range(1, last_index + 2), nrows = NROWS + 1)
    else: #Sinon, on en récupère le plus possible
        df_communes = pd.read_csv(DATASET_FILE, sep=';', encoding='utf-8', dtype=str, skiprows=range(1, last_index + 2))
        
    #Echantillon total n
    n = df_communes.shape[0]

    #Prise du temps au début du processus
    start_time = time.time()
    #Boucle principale du processus
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as pool:
        df_communes['url'] = list(tqdm.tqdm(pool.map(get_url, df_communes['nom'].values, df_communes['dep'].values, df_communes['code'].values), total=n))
    #Prise du temps à la fin du processus
    end_time = time.time()
    total_time = datetime.timedelta(seconds=end_time-start_time)
    #Affichage du temps total
    print(f"The operation took {total_time} \n")

    #On supprime les lignes n'ayant pas d'url
    df_communes = df_communes[df_communes['url'].notna()]
    
    #Sauvegarde du CSV
    csv_utils.save_to_csv(df_communes, CSV_FILE)