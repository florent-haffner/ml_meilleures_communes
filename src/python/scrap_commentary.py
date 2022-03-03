import requests
from bs4 import BeautifulSoup


def get_commentary_from_params(lien, insee):
  """
  :param lien :
  :param insee : french code that represent 
  """
  #Récupère les commerces
  chiffre = requests.get(lien).text
  soup = BeautifulSoup(chiffre, "html.parser")
  services = soup.find("section",{"id":"services"})
  all_tab_html=services.findAll("td")
  dico_service={}
  for i in all_tab_html :
      if (str(i.contents[0])=='<i class="fas fa-times"></i>'):
          dico_service[j]=0
      elif (i.contents[0].isdigit()) :
          dico_service[j]=int(i.contents[0])
      else :
          j=str(i.contents[0]).replace('\t','').replace('\n','')
      
  df_service=pd.DataFrame(dico_service, index=[0])

  #Récupère info Ville
  chiffre_web = soup.find_all('section', id='chiffres')

  Insee = insee
  Ville = []
  Code_postal = []
  Nb_habitants = []
  Superficie = []
  Pop_densite = []
  Pop_active = []
  Taux_chomage = []
  Revenu_moyen = []
  Prix_moyen = []
  Tranche_population_0_14 = []
  Activite_professionnelle = [] 
  Note_global = [] 

  for comp in chiffre_web:
      Ville.append(soup.find_all('h1')[0].text.strip()[:-6])
      Code_postal.append(soup.find_all('h1')[0].text.strip()[-5:])
      Nb_habitants.append(soup.find_all('td')[1].text.strip())
      Superficie.append(soup.find_all('td')[4].text.strip())
      Pop_densite.append(soup.find_all('td')[7].text.strip())
      Pop_active.append(soup.find_all('td')[10].text.strip())
      Taux_chomage.append(soup.find_all('td')[13].text.strip())
      Revenu_moyen.append(soup.find_all('td')[16].text.strip())
      Prix_moyen.append(soup.find_all('td')[19].text.strip())
      if(soup.find("canvas",id="chart_age")["data-data"] is not None):
        Tranche_population_0_14.append(soup.find("canvas",id="chart_age")["data-data"])
      else :
        Tranche_population_0_14.append(np.nan)
      Activite_professionnelle.append(soup.find("canvas",id="chart_metier")["data-data"])
      if (soup.find("div", {"class": "total compteur"}) is not None ):
        Note_global.append(soup.find("div", {"class": "total compteur"}).contents[0])
      else :
        Note_global.append(np.nan)
  #creating dataframe for all list
  features = {'Insee':Insee, 'Code_postal':Code_postal, 'Ville':Ville,  'Nb_habitants':Nb_habitants, 'Superficie':Superficie, 'Pop_densite':Pop_densite,
            'Pop_active':Pop_active, 'Taux_chomage':Taux_chomage, 'Revenu_moyen':Revenu_moyen, 'Prix_moyen':Prix_moyen,
            'Tranche_population_0_14':Tranche_population_0_14, 'Activite_professionnelle':Activite_professionnelle,
            'Note_global':Note_global}
  df = pd.DataFrame(features)

  #Creation d'un nouveau dataframe pour les tranches de populations
  dfTranche_population=df['Tranche_population_0_14']
  dfTranche_population = dfTranche_population.str[1:-1]
  TotListeAge = dfTranche_population.str.split(",").apply(pd.Series)
  TotListeAge
  listeAge = ['0-14 ans','15-29 ans', '30-44 ans', '45-59 ans','60-74 ans','75-89 ans','90+ ans']
  dfListeAgeNom=pd.DataFrame(listeAge)
  dfListeAgeNom=dfListeAgeNom.transpose()
  dfListeAge=pd.concat([dfListeAgeNom, TotListeAge])
  headers = dfListeAge.iloc[0]
  dfListeAge  = pd.DataFrame(dfListeAge.values[1:], columns=headers)
  dfListeAge

  #Creation d'un nouveau dataframe pour les activités professionelle
  dfActivite_professionnelle=df['Activite_professionnelle']
  dfActivite_professionnelle = dfActivite_professionnelle.str[1:-1]
  TotActivites = dfActivite_professionnelle.str.split(",").apply(pd.Series)
  TotActivites
  listeActivites = ['Agriculteurs','Artisants/Commercants', 'Cadres', 'Profession intermédiaire','Employes','Ouvriers','Retraites','Sans emploie']
  dfActivitesNom=pd.DataFrame(listeActivites)
  dfActivitesNom=dfActivitesNom.transpose()
  dfListeActivites=pd.concat([dfActivitesNom, TotActivites])
  headersActivites = dfListeActivites.iloc[0]
  dfListeActivites  = pd.DataFrame(dfListeActivites.values[1:], columns=headersActivites)
  dfListeActivites

  #récupère les notes des avis
  webpage = requests.get(lien+'/avis.html').text
  soupavis = BeautifulSoup(webpage, "html.parser")
  intro = soupavis.find("section", {"id": "intro"})
  notesHtml=intro.findAll("span",{"class":"compteur"})
  dicoNotes={}
  tabCategorie=["Securite", "Education","Loisir / Sport","Environnement","Pratique"]
  j=0
  for i in notesHtml :
      dicoNotes[tabCategorie[j]]=float(i.contents[0])
      j+=1
  dfNote=pd.DataFrame(dicoNotes, index=[0])

  #Créer un dataframe des commentaire
  com = soupavis.findAll("div",{"class":"commentaire"})
  avis = []
  for i in com :
    dico_com={}
    dico_com['Insee']=df['Insee'][0]
    dico_com['Code_postal']=df['Code_postal'][0]
    dico_com['Ville']=df['Ville'][0]
    k=0
    for j in i.findAll("span"):  
      if(j.has_attr('title')) :
        dico_com[j['title']]=int(j.contents[0])
      elif (k==0 and not j.has_attr('class')):
        dico_com['pouce_positif']=int(j.contents[0])
        k+=1
      elif( not j.has_attr('class')):
        dico_com['pouce_negatif']=int(j.contents[0])
    dico_com['commentaire']=i.find('p',{'class':'description'}).contents[0]
    dico_com['date']=i.find('div',{'class':'date'}).contents[0]
    dico_com['auteur']=i.find('div',{'class':'auteur'}).contents[0]
    avis.append(dico_com)
  df_com=pd.DataFrame(avis)
  

  dfConcat=pd.concat([df, dfListeActivites,dfListeAge,dfNote,df_service], axis=1)
  dfConcat=dfConcat.drop(columns=['Tranche_population_0_14','Activite_professionnelle'],axis=1)
  return dfConcat, df_com


if __name__ == '__main__':
    # Params
    url = 'https://www.bien-dans-ma-ville.fr/erstein-67130/avis.html'
    insee_code = '67130'

    # TODO - careful with this code, it's a copy paste and I couldn't start the script
    get_commentary_from_params(url, insee_code)
