import datetime
from re import I
from time import time

from datetime import date, timedelta, datetime

import requetes_blq_test as req

# Initialisation
erreurs : list = []

import sys
sys.path.append("/var/www/html/projets/bureau-laurent-quancard/gestion-des-offres/gestion_tarifs_automatises/Tarifs/batchs")
import nomenclature_bd_blq as nom

#Pour rajouter la bibliothèque numpy : python3 -m pip install numpy
import numpy as np

tab_profils : list = req.recuperation_profils_negociants()
tab_stock_offres : list = req.recuperation_tab( nom.stock_offres_str )
tab_partenaire : list = req.recuperation_tab( nom.partenaire_str )

tab_vins : list = req.recuperation_tab( nom.vin_str )
tab_vins_inverse : list = list(map(list, np.transpose(tab_vins)))

tab_millesimes : list = req.recuperation_tab( nom.millesime_str )
tab_millesimes_inverse : list = list(map(list, np.transpose(tab_millesimes)))

tab_formats_bouteille : list = req.recuperation_tab( nom.format_bouteille_str )
tab_formats_bouteille_inverse : list = list(map(list, np.transpose(tab_formats_bouteille)))

tab_conditionnements : list = req.recuperation_tab( nom.conditionnement_str )
tab_conditionnements_inverse : list = list(map(list, np.transpose(tab_conditionnements)))

# A voir si c'est utile de rajouter stock, partenaire et d'autres tables
tab_inverse_stock_offres : list = [tab_vins_inverse, tab_millesimes_inverse, tab_formats_bouteille_inverse, tab_conditionnements_inverse]

def recup_val_tab_inv(indice_tab_inverse : int, id_champ : int, mot_clef):

    # Rappel de la position des tables dans tab_inverse_stock_offres
    tab_inverse_stock_offres : list = [tab_vins_inverse, tab_millesimes_inverse, tab_formats_bouteille_inverse, tab_conditionnements_inverse]

    # tab_inverse_stock_offres : list = tab_inverse_stock_offres[ indice_tab_inverse ]

    id_element_en_base : int = -1

    # print("mot_clef : " + str(mot_clef))

    try:
        mot_clef = mot_clef.upper()

        if( mot_clef.isnumeric() ):
            # print("Passe")

            indice_ligne : int = tab_inverse_stock_offres[ id_champ ].index( int (mot_clef) )
            id_element_en_base = tab_inverse_stock_offres[ 0 ][ indice_ligne ]
            return id_element_en_base
        
        indice_ligne : int = tab_inverse_stock_offres[ id_champ ].index( mot_clef )
        id_element_en_base = tab_inverse_stock_offres[ 0 ][ indice_ligne ]
        # return id_element_en_base

    except BaseException as be:
        erreurs.append(be)

    return id_element_en_base

# Celle-ci a utiliser
def recup_val_tab_inv2(tab_inverse : list, id_champ : int, mot_clef):
    
    id_element_en_base : int = -1

    # print("id_element_en_base 1 " + str(id_element_en_base))

    # print("mot_clef : " + str(mot_clef))

    try:
        mot_clef = mot_clef.upper()

        if( mot_clef.isnumeric() ):
            # print("Passe")

            indice_ligne : int = tab_inverse[ id_champ ].index( int (mot_clef) )
            id_element_en_base = tab_inverse[ 0 ][ indice_ligne ]

            # print("id_element_en_base 2 " + str(id_element_en_base))

            return id_element_en_base
        
        indice_ligne : int = tab_inverse[ id_champ ].index( mot_clef )
        id_element_en_base = tab_inverse[ 0 ][ indice_ligne ]

        # print("id_element_en_base 3 " + str(id_element_en_base))
        # return id_element_en_base

    except BaseException as be:
        erreurs.append(be)

    # print("id_element_en_base 4 " + str(id_element_en_base))

    return id_element_en_base

def indice_doublon(id_negociant, vin_id, format_bouteille_id, conditionnement_id, millesime_id):

    # print(id_negociant)
    # print(vin_id)
    # print(format_bouteille_id)
    # print(conditionnement_id)
    # print(commentaires)
    # print(millesime_id)

    # Tester avant s'il y a déjà un vin avec un tarif !!!
    tuple_valeurs : tuple = (id_negociant, vin_id, millesime_id, format_bouteille_id, conditionnement_id)

    # requete = f"""SELECT stock_id, type_tarif_id FROM tarif 
    # WHERE stock_id = %s AND type_tarif_id = %s;"""

    # resultat : int = req.envoie_requete_tuple_avec_retour(requete, tuple_valeurs)[0][0]

    requete = f"""SELECT id FROM """ + nom.stock_offres_str + """ 
    WHERE partenaire_vendeur_id = %s  
    AND vin_id = %s 
    AND millesime_id = %s 
    AND format_id = %s 
    AND conditionnement_id = %s;"""

    retour_requete = req.envoie_requete_tuple_avec_retour(requete, tuple_valeurs)

    # print("retour_requete")
    # print(retour_requete)

    return retour_requete[0][0]

def modification_tarif(commentaires, indice, nom_table_tarif, type_tarif_id, quantite, prix):
    # print("Modification")

    date_datetime = datetime.now()
    
    # requete modifier stock_offres
    requete = f"""UPDATE """ + nom.stock_offres_str + """ 
    SET commentaires = '{commentaires}', date_maj = '{date_datetime}'
    WHERE id = '{indice}';"""

    req.envoie_requete_sans_retour(requete)

    # Tester avant s'il y a déjà un vin avec un tarif !!!
    tuple_valeurs : tuple = (indice, type_tarif_id)

    requete = f"""SELECT stock_id, type_tarif_id FROM tarif 
    WHERE stock_id = %s AND type_tarif_id = %s;"""

    resultat : int = req.envoie_requete_tuple_avec_retour(requete, tuple_valeurs)[0][0]

    # print("resultat : " + str(resultat))

    # date_datetime = datetime.now()

    if( resultat == -1):
        # insérer dans la table tarif

        # requete modifier tarif
        tuple_valeurs = (indice, type_tarif_id, quantite, prix)

        requete = f"""INSERT INTO tarif 
        (stock_id, type_tarif_id, quantite, prix) VALUES (%s, %s, %s, %s);"""

        req.envoie_requete_tuple_sans_retour(requete, tuple_valeurs)

        return
    
    # modifier dans la table tarif

    # requete modifier tarif
    tuple_valeurs = (quantite, prix, indice)

    requete = f"""UPDATE tarif 
    SET quantite = %s, prix = %s 
    WHERE stock_id = %s"""

    req.envoie_requete_tuple_sans_retour(requete, tuple_valeurs)

    return

erreurs_str : str= "ERREURS : "

def recup_max (nomColonne : str, nomTable : str):
    tuple_valeurs : tuple = (nomColonne, nomTable)
    requete = f"""SELECT MAX(""" + nomColonne + """) FROM """ + nomTable + """;"""

    return (req.envoie_requete_avec_retour(requete)[0][0])

def insertion_tarif(type_flux, nom_tarif_profil, vin : str, millesime : str, formatB : str , prix : float, quantite : int, conditionnement : str,commentaires, partenaire_vendeur_id : int):
    
    # Le premier élément sera : "ERREURS : "
    erreurs.append(erreurs_str)

    # vin_id
    # print("vin : " + vin)
    # vin_id : int = recup_val_tab_inv(0, 1, vin)
    vin_id : int = req.recuperation_un_id(nom.vin_str, "nom", vin)
    # print("Retour id vin : " + str(vin_id))

    # millesime_id
    # print("millesime : " + str(millesime))
    # millesime_id : int = recup_val_tab_inv(1, 1, millesime)
    millesime_id : int = req.recuperation_un_id(nom.millesime_str, "millesime", str(millesime))
    # print("Retour id millesime : " + str(millesime_id))

    # format_id
    # print("formatB : " + str(formatB))
    # format_id : int = recup_val_tab_inv(2, 1, formatB)
    format_id : int = req.recuperation_un_id(nom.format_bouteille_str, "format_bouteille", formatB)
    # print("Retour id format : " + str(format_id))

    # conditionnement_id
    # print("conditionnement : " + str(conditionnement))
    # conditionnement_id : int = recup_val_tab_inv(3, 1, conditionnement)
    conditionnement_id : int = req.recuperation_un_id(nom.conditionnement_str, "conditionnement", conditionnement)
    # print("Retour id conditionnement : " + str(conditionnement_id))

    # Test pour insertion dans stock_offres
    # erreurs = test_insertion_tarif(partenaire_vendeur_id, vin_id, format_id, conditionnement_id, millesime_id, erreurs)

    if( (vin_id == -1) or (millesime_id == -1) or (format_id == -1) or (conditionnement_id == -1) ):
        # print("vin : " + vin)
        # print("conditionnement : " + conditionnement)
        # print("vin_id : " + str(vin_id) + "- millesime_id : " + str(millesime_id) + "- format_id : " + str(format_id) + "- conditionnement_id : " + str(conditionnement_id))
        return
        # raise Exception('spam', 'eggs')

    if(erreurs[0] != erreurs_str):
        # print(erreurs)
        return

    # print("partenaire_vendeur_id : " + str(partenaire_vendeur_id))
    indice : int = indice_doublon(partenaire_vendeur_id, vin_id, format_id, conditionnement_id, conditionnement_id)
    # print("Retour indice : " + str(indice))

    nom_table_tarif = "" 

    # Choix du type de tarif
    tab_nom_table_tarif = ['tarif_officiel_stock', 'tarif_officieux_stock', 'tarif_export_stock']

    if(True):
        type_tarif_id : int = 1
    elif(False):
        type_tarif_id : int  = 2
    elif(False):
        type_tarif_id : int  = 3

    nom_table_tarif = "tarif"

    # print("quantite : " + str(quantite))
    # print("prix : " + str(prix))
    # print("indice : " + str(indice))

    # Trouvé ? : Modification sinon Insertion
    if(indice != -1):

        # print("modification vin -> modification tarif ou création tarif")
        # print("Modifier !!")

        modification_tarif(commentaires, indice, nom_table_tarif, type_tarif_id, quantite, prix)
        return

    # print("Créer !!")

    # print("creation vin")

    # print("partenaire_vendeur_id : " + str(partenaire_vendeur_id))

    commentaires = "commentaires"

    # print(str(partenaire_vendeur_id)  + " : " + str(vin_id)  + " : " + str(millesime_id)  + " : " + str(format_id)  + " : " + str(conditionnement_id)  + " : " + str(commentaires))

    #requete insert stock_offres
    tuple_valeurs : tuple = (partenaire_vendeur_id, vin_id, millesime_id, format_id, conditionnement_id, commentaires)
    requete : str = f"""INSERT INTO """ + nom.stock_offres_str + """ (partenaire_vendeur_id, vin_id, millesime_id, format_id, conditionnement_id, commentaires) VALUES (%s, %s, %s, %s, %s, %s);"""
    req.envoie_requete_tuple_sans_retour(requete, tuple_valeurs)

    # print("insertion stock_offres OK")

    # requete récupération de l'indice ( = indice max de la table)
    max_id_stock : int = recup_max("id", nom.stock_offres_str)

    # print("max_id_stock : " + str(max_id_stock))

    # requete insérer tarif
    tuple_valeurs : tuple = (max_id_stock, type_tarif_id, int(quantite), float(prix))
    requete = f"""INSERT INTO tarif(stock_id, type_tarif_id, quantite, prix) VALUES (%s, %s, %s, %s)"""
    req.envoie_requete_tuple_sans_retour(requete, tuple_valeurs)




