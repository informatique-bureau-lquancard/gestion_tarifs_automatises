
from tests_tarifs import traitement_tarifs_flux as trt

import initialisation_blq as init
# from models import Profil

# Fichier regroupant les requêtes (et l'accès à la base : à améliorer )
import requetes_blq as req

# Pour rajouter la bibliothèque numpy : python3 -m pip install numpy
# Permet d'inverser les tableaux
import numpy as np

# php a enlevé // A changer
chemin_dossier_tarifs : str = "/var/www/html/projets/bureau-laurent-quancard/gestion-des-offres/gestion_tarifs_automatises/Tarifs/"

# A revoir utilité !! remplacer par 
dossier_sortie : str = "tarifs_HEBDO"

import sys
sys.path.append("/var/www/html/projets/bureau-laurent-quancard/gestion-des-offres/gestion_tarifs_automatises/Tarifs/batchs")
import nomenclature_bd_blq as nom

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

print("Hello Python")

def traitement_tarif():

    print("Fin initialisation")
    
    # Table profil : id, profil, chemin, flux, type_tarif_id, flux_id, partenaire_id
    for profil in tab_profils:

        # profil[5] = nom du flux
        if profil[5] == 'XML':
            
            # profil[0] = profil // ne servira plus quand on aura fusionné les traitement des fichiers pour le XML
            if profil[0] == 'MILIMA':

                # profil[2] = nom du flux # profil[1] = nom dossier # profil[0] = profil # profil[7] = id negociant
                script_tarif = trt.fct_flux_tree_xml_1(profil[2], chemin_dossier_tarifs + dossier_sortie + "/sortie_" + profil[0] + ".csv", profil[0], profil[7])

            elif( profil[0] == 'ANGWIN_HEBDO'):
                print("No")
                # script_tarif = trt.fct_flux_tree_xml_2(profil[2], chemin_dossier_tarifs + dossier_sortie + "/sortie_" + profil[0] + ".csv", profil[0], profil[7])

        elif(profil[5] == 'GOOGLE SHEETS'):
            
            if( profil[0] == 'CUVFAU'):

                script_tarif = trt.fct_flux_google_sheets1(profil[2], chemin_dossier_tarifs + dossier_sortie + "/sortie_" + profil[0], profil[0], profil[7])

            elif( profil[0] == 'MAISOB'):

                script_tarif = trt.fct_flux_google_sheets2(profil[2], chemin_dossier_tarifs + dossier_sortie + "/sortie_" + profil[0], profil[0], profil[7])
                

