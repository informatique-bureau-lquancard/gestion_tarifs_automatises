import feedparser
from lxml import etree
import csv
import sys

sys.path.append("/var/www/html/projets/bureau-laurent-quancard/gestion-des-offres/gestion_tarifs_automatises/Tarifs/batchs/fonctions_profils")
import specifiques_xml as sx

import peuplement_de_la_base as pb

import sys
sys.path.append("/var/www/html/php/fonctions_tarifs")
import Fonction_tarifs as ft

from unidecode import unidecode

def fin(writer, type_flux_id, nom_tarif_profil, offre : pb.Offre.Offre):
    # insertion des lignes dans la base
    pb.insertion_tarif(type_flux_id, nom_tarif_profil, offre)

    writer.writerow( [offre.vin, offre.millesime, offre.formatB, offre.prix, offre.quantite, offre.conditionnement, offre.commentaires] )

def general_xml(flux, chemin_fichier_sortie, nom_tarif_profil, id_negociant):
    
    type_flux_id = 1

    tree = etree.parse(flux)

    #Vin = etree.Element("Produit")

    with open(chemin_fichier_sortie,'w',newline='', encoding='utf-8') as monFichierSortie:
        writer = csv.writer(monFichierSortie, delimiter=';', quoting=csv.QUOTE_NONE, escapechar=';', quotechar='')

        xpath_str : str = ""

        if( nom_tarif_profil == "MILIMA"):
            xpath_str = "/XMLFILE/Produit"

        treepath = tree.xpath( xpath_str )

        for Vin in treepath :
            
            if( nom_tarif_profil == "MILIMA"):
                [vin,millesime,formatB,prix,quantite,conditionnement,commentaires] = sx.specifique1( Vin )

            offre : pb.Offre.Offre = pb.Offre.Offre(id_negociant, [vin,millesime,formatB,prix,quantite,conditionnement,commentaires])

            fin(writer, type_flux_id, nom_tarif_profil, offre)

            print("insertion !!")

        return writer

def general_xml2(type_flux_id, chemin_fichier_sortie, nom_tarif_profil, id_negociant):
        
    feed = feedparser.parse(type_flux_id)

    # tree = etree.parse(type_flux_id)

    with open(chemin_fichier_sortie,'w',newline='', encoding='utf-8') as monFichierSortie:
        writer = csv.writer(monFichierSortie, delimiter=';', quoting=csv.QUOTE_NONE, escapechar=';', quotechar='')

        # treepath = tree.xpath('.//table[@class="W(100%)"]/channel/item')
    
        for entry in feed.entries:

            if( nom_tarif_profil == "ANGWIN_HEBDO"):
                [vin,millesime,formatB,prix,quantite,conditionnement,commentaires] = sx.specifique2( entry )

            offre : pb.Offre = pb.Offre(id_negociant, [vin,millesime,formatB,prix,quantite,conditionnement,commentaires])
            
            fin(writer, type_flux_id, nom_tarif_profil, offre)

            print("insertion !!")

        return writer
