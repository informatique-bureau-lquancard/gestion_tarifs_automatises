import datetime
from re import I
from time import time

from datetime import datetime

import requetes_blq_test as req

# Initialisation
erreurs : list = []

import sys
sys.path.append("/var/www/html/projets/bureau-laurent-quancard/gestion-des-offres/gestion_tarifs_automatises/Tarifs/batchs")
import nomenclature_bd_blq as nom

sys.path.append("/var/www/html/php/fonctions_tarifs/Fonction_tarifs.py")
import Fonction_tarifs as ft

sys.path.append("/var/www/html/projets/bureau-laurent-quancard/gestion-des-offres/gestion_tarifs_automatises/Tarifs/batchs/fonctions_profils/model")
import Offre

import numpy as np

from unidecode import unidecode

tab_vins : list = req.recuperation_tab( nom.vin_str )
tab_vins_inverse : list = list(map(list, np.transpose(tab_vins)))

tab_millesimes : list = req.recuperation_tab( nom.millesime_str )
tab_millesimes_inverse : list = list(map(list, np.transpose(tab_millesimes)))

tab_formats_bouteille : list = req.recuperation_tab( nom.format_bouteille_str )
tab_formats_bouteille_inverse : list = list(map(list, np.transpose(tab_formats_bouteille)))

tab_conditionnements : list = req.recuperation_tab( nom.conditionnement_str )
tab_conditionnements_inverse : list = list(map(list, np.transpose(tab_conditionnements)))

class TestPeuplementDeLaBase():

    def __init__(self):
        print(type(self).__name__)

        # A retester
        type_tarif_id : int = 1

        nom_tarif_profil : str = ""

        id_negociant : int = 

        vin : str = "CHATEAU RAUZAN-GASSIES"
        millesime : int
        formatB : str
        prix : float
        quantite : int
        conditionnement : str
        commentaires : str

        offre : Offre = Offre(id_negociant, [vin,millesime,formatB,prix,quantite,conditionnement,commentaires])

        self.insertion_tarif(type_tarif_id, nom_tarif_profil, offre)

    def insertion_tarif(type_tarif_id, nom_tarif_profil, offre : Offre):
        
        # Le premier élément sera : "ERREURS : "
        erreurs.append(erreurs_str)

        # vin_id
        vin_id : int = req.recuperation_un_id(nom.vin_str, "nom", offre.vin)

        id : int = test2( offre.vin )

        # millesime_id
        millesime_id : int = req.recuperation_un_id(nom.millesime_str, "millesime", str(offre.millesime))

        # format_id
        format_id : int = req.recuperation_un_id(nom.format_bouteille_str, "format_bouteille", offre.formatB)

        # conditionnement_id
        conditionnement_id : int = req.recuperation_un_id(nom.conditionnement_str, "conditionnement", offre.conditionnement)

        if( (vin_id == -1) or (millesime_id == -1) or (format_id == -1) or (conditionnement_id == -1) ):
            return

        if(erreurs[0] != erreurs_str):
            return

        nom_table_tarif = "" 

        # Choix du type de tarif
        tab_nom_table_tarif = ['tarif_officiel_stock', 'tarif_officieux_stock', 'tarif_export_stock']

        if(True):
            type_tarif_id : int = 1

        commentaires = "commentaires"

        #requete insert stock_offres
        tuple_valeurs : tuple = (offre.partenaire_vendeur_id, vin_id, millesime_id, format_id, conditionnement_id, commentaires)
        requete : str = f"""INSERT INTO """ + nom.stock_offres_str + """ (partenaire_vendeur_id, vin_id, millesime_id, format_id, conditionnement_id, commentaires) VALUES (%s, %s, %s, %s, %s, %s);"""
        
        print("Création offre")
        print("vin_id : " + str(vin_id) + "- millesime_id : " + str(millesime_id) + "- format_id : " + str(format_id) + "- conditionnement_id : " + str(conditionnement_id))
        
        max_id_stock : int = recup_max("id", nom.stock_offres_str)

        # requete insérer tarif
        tuple_valeurs : tuple = (max_id_stock, type_tarif_id, int(offre.quantite), float(offre.prix))
        requete = f"""INSERT INTO tarif(stock_id, type_tarif_id, quantite, prix) VALUES (%s, %s, %s, %s)"""
        
        print("Création tarif")
        print("vin_id : " + str(vin_id) + "- millesime_id : " + str(millesime_id) + "- format_id : " + str(format_id) + "- conditionnement_id : " + str(conditionnement_id))
            
def test1():
    
    tab_vins_tansformee = [];

    # Possible conflit avec les traitements qui utilise ce fichier    
    if( len(tab_vins_inverse) == 0):
        return []

    for vin in tab_vins_inverse[1]:

        vin : str = unidecode( vin )

        tab_caracteres_a_supprimer = ["'", "-", "_", "CHATEAU"]

        vin = ft.supprimeChaineCaracteresAvecEspace( vin, tab_caracteres_a_supprimer )

        tab_vins_tansformee.append( vin )

    return tab_vins_tansformee

# Conflit avec traitement_domaines_vins.py Commenter/Decommenter
tab_vins_tansformee = test1();

def test2(chaine : str):

    list_chaine_split = chaine.split()

    i : int = 1

    stock_vin : list = []

    for element in tab_vins_tansformee :

        liste_element : list = element.split()

        comparaison : list = list( set( list_chaine_split ) & set( liste_element ) )

        if( comparaison == liste_element ):

            return i

        stock_vin.append( [ element, i , len( comparaison )] )

        i = i + 1

    if( len( comparaison ) == 0 ):

        return -1

    stock_vin_inverse = list(map(list, np.transpose(stock_vin)))

    max = max( stock_vin_inverse[2] )
    id_max : int = stock_vin_inverse[2].index( max )

    return id_max

def recup_val_tab_inv(indice_tab_inverse : int, id_champ : int, mot_clef):

    # Rappel de la position des tables dans tab_inverse_stock_offres
    tab_inverse_stock_offres : list = [tab_vins_inverse, tab_millesimes_inverse, tab_formats_bouteille_inverse, tab_conditionnements_inverse]

    id_element_en_base : int = -1

    try:
        mot_clef = mot_clef.upper()

        if( mot_clef.isnumeric() ):

            indice_ligne : int = tab_inverse_stock_offres[ id_champ ].index( int (mot_clef) )
            id_element_en_base = tab_inverse_stock_offres[ 0 ][ indice_ligne ]
            return id_element_en_base
        
        indice_ligne : int = tab_inverse_stock_offres[ id_champ ].index( mot_clef )
        id_element_en_base = tab_inverse_stock_offres[ 0 ][ indice_ligne ]

    except BaseException as be:
        erreurs.append(be)

    return id_element_en_base

# Celle-ci a utiliser
def recup_val_tab_inv2(tab_inverse : list, id_champ : int, mot_clef):
    
    id_element_en_base : int = -1

    try:
        mot_clef = mot_clef.upper()

        if( mot_clef.isnumeric() ):

            indice_ligne : int = tab_inverse[ id_champ ].index( int (mot_clef) )
            id_element_en_base = tab_inverse[ 0 ][ indice_ligne ]

            return id_element_en_base
        
        indice_ligne : int = tab_inverse[ id_champ ].index( mot_clef )
        id_element_en_base = tab_inverse[ 0 ][ indice_ligne ]

    except BaseException as be:
        erreurs.append(be)

    return id_element_en_base

def indice_doublon(id_negociant, vin_id, format_bouteille_id, conditionnement_id, millesime_id):

    # Tester avant s'il y a déjà un vin avec un tarif !!!
    tuple_valeurs : tuple = (id_negociant, vin_id, millesime_id, format_bouteille_id, conditionnement_id)

    requete = f"""SELECT id FROM """ + nom.stock_offres_str + """ 
    WHERE partenaire_vendeur_id = %s  
    AND vin_id = %s 
    AND millesime_id = %s 
    AND format_id = %s 
    AND conditionnement_id = %s;"""

    retour_requete = req.envoie_requete_tuple_avec_retour(requete, tuple_valeurs)

    return retour_requete[0][0]

def modification_tarif(commentaires, indice, nom_table_tarif, type_tarif_id, quantite, prix):

    date_datetime = datetime.now()
    
    # requete modifier stock_offres
    requete = f"""UPDATE """ + nom.stock_offres_str + """ 
    SET commentaires = '{commentaires}', date_maj = '{date_datetime}'
    WHERE id = '{indice}';"""

    print("modification_tarif 1 ")

    # Tester avant s'il y a déjà un vin avec un tarif !!!
    tuple_valeurs : tuple = (indice, type_tarif_id)

    requete = f"""SELECT stock_id, type_tarif_id FROM tarif 
    WHERE stock_id = %s AND type_tarif_id = %s;"""

    resultat : int = req.envoie_requete_tuple_avec_retour(requete, tuple_valeurs)[0][0]

    if( resultat == -1):

        # requete modifier tarif
        tuple_valeurs = (indice, type_tarif_id, quantite, prix)

        requete = f"""INSERT INTO tarif 
        (stock_id, type_tarif_id, quantite, prix) VALUES (%s, %s, %s, %s);"""

        print("Création du tarif")
        print("indice : " + str(indice) + "- type_tarif_id : " + str(type_tarif_id) + "- quantite : " + str(quantite) + "- prix : " + str(prix))

        return
    
    # modifier dans la table tarif
    tuple_valeurs = (quantite, prix, indice)

    requete = f"""UPDATE tarif 
    SET quantite = %s, prix = %s 
    WHERE stock_id = %s"""

    print("Modification du tarif")
    print("quantite : " + str(quantite) + "- prix : " + str(prix) + "- indice : " + str(indice))
        
    return

erreurs_str : str= "ERREURS : "

def recup_max (nomColonne : str, nomTable : str):
    tuple_valeurs : tuple = (nomColonne, nomTable)
    requete = f"""SELECT MAX(""" + nomColonne + """) FROM """ + nomTable + """;"""

    return (req.envoie_requete_avec_retour(requete)[0][0])






