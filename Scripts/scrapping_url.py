#Imports
import pandas as pd
import tqdm
import urllib.request
import time
import datetime
import concurrent.futures
from random import randint
from time import sleep

#Constantes
DATASET_FILE = './Resources/communes_short.csv'
CSV_FILE = './Resources/communes_url.csv'

def get_url(nom, dep, code):
    url = f"https://www.bien-dans-ma-ville.fr/{nom}-{dep}-{code}"
    try:
        fp = urllib.request.urlopen(url)
        fp.close()
        sleep(randint(1,5)) #Permet d'éviter le ban ip du site (Côté négatif, rallonge le temps de traitement)
        return url
    except urllib.error.HTTPError as exception: #On gère l'erreur 404 et on ajoute l'index dans notre liste
        pass

if __name__ == '__main__':
    #Lecture du CSV contenant les codes INSEE et les noms de communes
    df_communes = pd.read_csv(DATASET_FILE, sep=';', encoding='utf-8', dtype=str)

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
    print("\nThe operation took {0}".format(total_time))

    #On supprime les lignes n'ayant pas d'HTML
    df_communes = df_communes[df_communes['url'].notna()]
        
    #Sauvegarde des nouvelles données dans un nouveau csv
    df_communes.to_csv(CSV_FILE, sep=';', encoding='utf-8', index=False)