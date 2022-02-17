#Imports
import pandas as pd
import urllib.request
import time
import datetime
from Utils.progress_bar import progressBar

#Lecture du CSV contenant les codes INSEE et les noms de communes
df_communes = pd.read_csv('./Resources/communes_short.csv', sep=';', encoding='utf-8', nrows=100)

#Echantillon total n
n = df_communes.shape[0]

#Si la colonne 'url' n'existe pas, on la créé
if 'url' not in df_communes:
    df_communes["url"] = "" #Cette colonne contiendra les URL valides récupérées
   
indexes_to_drop = []
start_time = time.time()
for index, commune in progressBar(n, df_communes.iterrows(),prefix = 'Progress:', suffix = 'Complete', length = 50):
    try:
        url = "https://www.bien-dans-ma-ville.fr/{0}-{1}-{2}".format(commune[1], commune[2], commune[0])
        fp = urllib.request.urlopen(url)
        commune['url'] = url
        fp.close()
    except urllib.error.HTTPError as exception: #On gère l'erreur 404 et on ajoute l'index dans notre liste
        indexes_to_drop.append(index)
end_time = time.time()
total_time = datetime.timedelta(seconds=end_time-start_time)
print("\nThe operation took {0}".format(total_time))

#On supprime les lignes n'ayant pas d'HTML
for index in indexes_to_drop:
    df_communes = df_communes.drop(index)
    
#Sauvegarde des nouvelles données dans un nouveau csv
df_communes.to_csv('./Resources/communes_url.csv', sep=';', encoding='utf-8', index=False)