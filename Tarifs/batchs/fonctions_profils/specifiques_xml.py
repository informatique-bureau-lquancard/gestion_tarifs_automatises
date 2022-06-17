import re
import sys
sys.path.append("/var/www/html/php/fonctions_tarifs")
import Fonction_tarifs as ft

from unidecode import unidecode

def specifique1( Vin ):

    # couleur
    couleur : str = (Vin[4].text).upper()

    # vin, enlève la date de vin
    vin : str = unidecode((Vin[0].text)[:-5])

    vin = ft.formaterVin("", vin, couleur)

    # millesime
    millesime : str = ft.formaterAnnee( Vin[1].text )

    # foramtB
    formatB : str = ft.formaterFormatBouteilleBis( Vin[9].text )

    # prix
    qCaisse : str = Vin[18].text
    iNb : int = qCaisse.find("*")
    qCaisse = qCaisse[:int(iNb)].replace(" ","")

    fprix : str = Vin[7].text
    fprix = float(fprix) / int(qCaisse)
    prix : str = str(fprix)
    prix = prix.replace(",",".")

    prix_float : float = round(float(prix), 2)
    prix = str(prix_float)

    # quantite
    quantite : str = Vin[17].text

    # conditionnement

    conditionnement : str = ft.formaterConditionnement(formatB, int(quantite), Vin[10].text, vin)
    conditionnement : str = conditionnement.replace("CCO", 'CC')

    # Mise à jour qui ont rendu inutilisable les conditionnements
    # conditionnement = ft.formatterConditionnement(formatB, quantite, conditionnement, vin)

    # commentaires
    commentaires : str = ""

    if( (conditionnement not in ft.tab_conditionnement) and ( conditionnement == "CBO24DE" ) ):
        commentaires = "VERIF CDT - "+conditionnement

    return [vin,millesime,formatB,prix,quantite,conditionnement,commentaires]

def specifique2( entry ):

    item = entry.description

    prix_ttc : str = ft.formaterPrix( entry.g_price )
    # Erreur ici !!
    prix_ht : float = float(prix_ttc.replace(',','.'))/float(1.2)
    # à revoir les prix
    # prix_ht : float = round(float(prix), 2)
    prix : str = str(prix_ht).replace(',','.')

    quantite = entry.g_sell_on_google_quantity
    couleur = entry.g_color

    rec_millesime = re.findall('[0-9][0-9][0-9][0-9]',item)
    millesime = rec_millesime[0] if rec_millesime else 'NV'
    
    vin = unidecode(item.split(millesime)[0]).replace(';','')
    vin = vin.upper()
    
    rec_formatB = re.findall('[0-9]?[,]?[0-9][eE0-9][cC]?[lL]',item)

    formatB_dict = ['Magnum','Double Magnum', 'Jeroboam', 'Imper']
    formatB = ''

    for f in formatB_dict :

        if f not in item :
            break

        iFormat = item.find(f)
        formatB = item[int(iFormat):]

    if rec_formatB and formatB == '':
        formatB = rec_formatB[0]
    elif 'Imperiale' in item :
        formatB = 'IM'
    elif formatB == '' :
        formatB = 'BO'

    formatB : str = ft.formaterFormatBouteille(formatB)

    conditionnement : str = ft.conditionnementParDefaut(formatB,int(quantite))
    commentaires : str = 'Verif CDT'

    return [vin,millesime,formatB,prix,quantite,conditionnement,commentaires]
                
            