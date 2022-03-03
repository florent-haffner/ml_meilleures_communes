import os
import pandas as pd

def save_to_csv(df, file):
    """Sauvegarder le dataframe donné au chemin donné

    Args:
        df (Pandas.DataFrame): DataFrame a sauvegarder
        file (str): Chemin du fichier
    """
    #Si le fichier existe déjà, on supprime la première ligne et on écrit en mode 'append'
    if os.path.isfile(file):
        df.to_csv(file, sep=';', encoding='utf-8', header=None, index=False, mode='a')
    else:
        #Sinon on écrit en mode écriture (création/écrasement du fichier)
        df.to_csv(file, sep=';', encoding='utf-8', index=False, mode='w')
        
        
def get_last_index(file):
    """Retourne le dernier index présent dans le fichier ou -1 si le fichier n'existe pas

    Args:
        file (str): Chemin du fichier

    Returns:
        int: Valeur du dernier index
    """
    if os.path.isfile(file):
        #Lecture du CSV s'il existe
        df = pd.read_csv(file, sep=';', encoding='utf-8', dtype=str)
        return int(df.iloc[-1,0])
    else:
        #S'il n'existe pas on instancie la valeur du dernier index à -1 pour qu'il soit égal à 1 plus tard
        return -1