# Fichier regroupant les requêtes (et l'accès à la base : à améliorer )
import requetes_blq as req

#Pour rajouter la bibliothèque numpy : python3 -m pip install numpy
import numpy as np

# Tableau derepresentant les tables en base bd_blq

tab_partenaires = []
tab_partenaires_inverse = []

tab_domaines = []
tab_appellations = []

tab_types_partenaire = []
tab_pays = []

tab_stock_tarifs = []

tab_tarifs_officiel_stock = []
tab_tarifs_export_stock = []
tab_tarifs_officieux_stock = []

tab_utilisateurs = []

# A revoir , sert ??
indice_tarifs_different = 2

#nom du dossier des tarifs officiels
tarifs_HEBDO :str = 'tarifs_HEBDO'
#nom du dossier des tarifs export
tarifs_EXPORT :str = 'tarifs_EXPORT'
#nom du dossier des tarifs officieux
tarifs_AUTRES :str = 'tarifs_AUTRES'

# tarifs_hebdo_profil = ["profilA", "profilB", "profilC", "profilD"]

# tarifs_hebdo_negociants = ["negociantA", "negociantB", "negociantC", "negociantD"]

# #Création du dictionnaire negociants en fonction des profils 
# dict_profils_negociants = dict(zip(tarifs_hebdo_profil, tarifs_hebdo_negociants))

import sys
sys.path.append("/var/www/html/projets/bureau-laurent-quancard/gestion-des-offres/gestion_tarifs_automatises/Tarifs/batchs")
import nomenclature_bd_blq as nom

def init_table_base():
    print("ok init_table_base")

    tab_partenaires = req.recuperation_tab( nom.partenaire_str )
    #Inverse les lignes avec les colonnes : Pour travailler avec les colonnes plutôt qu'avec les lignes
    tab_partenaires_inverse = np.transpose(tab_partenaires)
    print("ok " + nom.partenaire_str)
    
    tab_domaines = req.recuperation_tab( nom.domaine_str )
    print("ok " + nom.domaine_str)
    tab_appellations = req.recuperation_tab( nom.appellation_str )
    print("ok " + nom.appellation_str)

    tab_types_partenaire = req.recuperation_tab( nom.type_partenaire_str )
    print("ok " + nom.type_partenaire_str)
    tab_pays = req.recuperation_tab( nom.pays_str )
    print("ok " + nom.pays_str)

    # tab_stock_tarifs = req.recuperation_tab('stock_tarifs')
    # print("ok stock_tarifs")
    # tab_tarifs_officiel_stock = req.recuperation_tab('tarif_officiel_stock')
    # print("ok tarif_officiel_stock")
    # tab_tarifs_export_stock = req.recuperation_tab('tarif_export_stock')
    # print("ok tarif_export_stock")
    # tab_tarifs_officieux_stock = req.recuperation_tab('tarif_officieux_stock')
    # print("ok tarif_officieux_stock")

    tab_utilisateurs = req.recuperation_tab( nom.utilisateur_str )
    print("ok " + nom.utilisateur_str)

    # tab_gestion_profil = req.recuperation_gestion_profil()
    # print("ok utilisateur")