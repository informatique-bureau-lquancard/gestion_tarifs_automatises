import datetime
from re import I
from time import time

from datetime import date, timedelta, datetime

import traitement_tarifs as tt
import requetes_blq as req

# Un problème de sauvegarde du fichier a été détecté, revoir la différence entre les deux fichiers et les fusionner


#On teste si l'offre existe déjà
# if(selection_offre):
#       #OUI on la modifie
#     modification_offre
# else:
#       #NON on l'insert dans la base
#     insertion_offre

def indice_doublon(id_negociant, vin_id, format_bouteille_id, conditionnement_id, commentaires, millesime_id):

    print(id_negociant)
    print(vin_id)
    print(format_bouteille_id)
    print(conditionnement_id)
    print(commentaires)
    print(millesime_id)

    # Attention il faudra uniformiser les commentaires !!
    requete = f"""SELECT s.id FROM stock as s
    JOIN vin as v ON s.vin_id = v.id
    JOIN vin_millesime as vm ON v.id = vm.vin_id
    WHERE partenaire_vendeur_id = '{id_negociant}'  
    AND s.vin_id = '{vin_id}' 
    AND s.format_id = '{format_bouteille_id}' 
    AND s.conditionnement_id = '{conditionnement_id}' 
    AND s.commentaires = '{commentaires}' 
    AND vm.vin_id = '{vin_id}'
    AND vm.millesime_id = '{millesime_id}';"""

    retour_requete = req.envoie_requete_avec_retour(requete)

    print("retour_requete : doublon ")
    print(retour_requete)

    return retour_requete[0][0]

def modification_tarif(commentaires, indice, nom_table_tarif, quantite, prix):
    print("Modification")

    date_datetime = datetime.now()
    
    # requete modifier stock
    requete = f"""UPDATE stock 
    SET commentaires = '{commentaires}', date_maj = '{date_datetime}'
    WHERE id = '{indice}'"""

    req.envoie_requete_sans_retour(requete)

    # requete modifier tarif
    tuple_valeurs = (quantite, prix, indice)

    requete = f"""UPDATE """ + nom_table_tarif + """
    SET quantite = %s, prix = %s 
    WHERE id = %s"""

    req.envoie_requete_sans_retour2(requete, tuple_valeurs)

    return

# def insertion_tarif():
#     # Modification/Insertion stock
#         # Modification/Insertion stock
#         # Modification ou Insertion stock_tarif -> tarif_officiel_stock et tarif_officieux_stock et tarif_export_stock

#     return


erreurs_str : str= "ERREURS : "

# def test_insertion_tarif(partenaire_vendeur_id, vin_id, format_id, conditionnement_id, millesime_id, erreurs):

#     # Test pour insertion dans stock
#         # Test et modification partenaire -> pays et type_parteanaire
#         # Test et modification vin -> domaine et appellation et millesime
#         # Test et modification format_bouteille
#         # Test et modification conditionnement

#     # Peut-être amélioré en récupérant le nom de la variable, évite le dictionnaire
#     tab_id_stock = {"partenaire_vendeur_id": partenaire_vendeur_id, "vin_id": vin_id, "format_id": format_id, "conditionnement_id": conditionnement_id}

#     for clef, valeur in tab_id_stock:
#         erreurs += requete_test_modification_stock(clef, valeur)

#     return erreurs_str

# def requete_test_modification_stock(valeur_id_a_tester : int, champ : str):
#     requete = f"""SELECT '{champ}' FROM stock WHERE '{champ}' = '{valeur_id_a_tester}';"""

#     retour_requete = req.envoie_requete_avec_retour(requete)

#     if(retour_requete != ""):
#         return champ + " " + retour_requete.__str__ + " "

#     return ""

def insertion_tarif(type_flux, nom_tarif_profil,vin,millesime,formatB,prix : float,quantite,conditionnement,commentaires,partenaire_vendeur_id):

    # Test pour insertion dans stock
        # Test et modification partenaire -> pays et type_parteanaire
        # Test et modification vin -> domaine et appellation et millesime
        # Test et modification format_bouteille
        # Test et modification conditionnement

    # Modification/Insertion stock
        # Modification/Insertion stock
        # Modification ou Insertion stock_tarif -> tarif_officiel_stock et tarif_officieux_stock et tarif_export_stock

    # Initialisation
    erreurs = []
    
    # Le premier élément sera : "ERREURS : "
    erreurs.append(erreurs_str)

    # Logique de création d'une ligne dans stock qui représente une offre de tarif

    # Alert quand il y en a pas en base II Puis correction manuelle II Site web pour corriger les tarifs.

    # Question a répondre : est-ce qu'il existe un vin avec les mêmes attributs ? (correction manuelle ? Les bons il rentrent les autres sont sauvegarder afin d'être traité manuellement)
    # OUI : récupérer l'id du vin
    # NON : le domaine existe ? # OUI récupérer l'id
                                # NON créer le domaine
    #       l'appellation existe ?  # OUI récupérer l'id
                                    # NON créer l'appelation
    #       le millesime existe ?   # OUI récupérer l'id
                                        # Le millesime se rapporte au même vin ?    # OUI ne rien faire
                                                                                    # NON créer vin_millesime
                                    # NON créer le millesime (d'autres tests par rapport à ce qu'à la table, exemple etiquette_id...)
                                        # récupérer l'id
                                        # créer vin_millesime

    # Connaître le type de tarif à enregistrer. (correction automatique)
    # Question a répondre : est-ce qu'il existe un tarif avec le même id qu une ligne dans stock ?
        # OUI : attributs changés (quantite, prix) ? # OUI Modifier le bon tarif par rapport à son type
        #                                            # NON créer un nouveau tarif de chaque types (officiel, officieux, export) -> Créer stock_tarifs
        # NON créer un nouveau tarif de chaque types (officiel, officiueux, export) -> Créer stock_tarifs

    # [1] : nom du vin
    try:
        vin : str = vin.upper()

        # Les tableaux commencent à l'indice 0 et les table dans la base de données à l'indice 1
        # La colonne nom est à l'indice 1
        vin_id :int = (tt.tab_vins_inverse[1].index(vin)) + 1

    except BaseException as be:
        erreurs.append(be)

    print("vin_id : " + str(vin_id))

    # [1] : millesime
    try:
        millesime_id : int = (tt.tab_millesimes_inverse[1].index(int(millesime))) + 1

    except BaseException as be:
        erreurs.append(be)

    print("millesime_id : " + str(millesime_id))

    # [1] : vin_millesime

    requete = f"""SELECT vin_id, millesime_id FROM vin_millesime WHERE (vin_id = '{vin_id}') and (millesime_id = '{millesime_id}');"""

    retour_requete = req.envoie_requete_avec_retour(requete)[0][0]

    print("retour_requete  vin_millesime : " + str(retour_requete))

    if(retour_requete == -1):

        # création
        tuple_valeurs = (vin_id, millesime_id)

        requete = f"""INSERT INTO vin_millesime(vin_id, millesime_id) VALUES (%s,%s);"""

        req.envoie_requete_sans_retour2(requete, tuple_valeurs)

    # [1] : formatB
    try:
        format_id = (tt.tab_formats_bouteille_inverse[1].index(formatB)) + 1

    except BaseException as be:
        erreurs.append(be)

    # [1] : conditionnement
    try:
        conditionnement_id = (tt.tab_conditionnements_inverse[1].index(conditionnement)) + 1

    except BaseException as be:
        erreurs.append(be)

    # Test pour insertion dans stock
    # erreurs = test_insertion_tarif(partenaire_vendeur_id, vin_id, format_id, conditionnement_id, millesime_id, erreurs)

    if(erreurs[0] != erreurs_str):
        print(erreurs)
        return

    # Modification/Insertion stock

    # 2 Description du test d'une ligne afin décrire en base
    #On ne veut pas de doublon dans la base, on supprime l'ancienne offre similaire
    #Les conditions pour tester l'égalité d'une offre sont : partenaire_vendeur.nom, vin.nom, millesime.annee, format_bouteille.format_bouteille, conditionnement.conditionnement, commentaires
    #Sur le test des commentaires on ne testera que la première partie du commentaire, que l'on remplira dans le cas où il y a plusieurs offres du même négociant
    #On peut mettre des nombres par exemple un nombre à trois chiffre 111. 112. 113

    indice : int = indice_doublon(partenaire_vendeur_id, vin_id, format_id, conditionnement_id, commentaires, millesime_id)

    nom_table_tarif = "" 

    # Choix du type de tarif
    tab_nom_table_tarif = ['tarif_officiel_stock', 'tarif_officieux_stock', 'tarif_export_stock']

    if(True):
        nom_table_tarif : str = tab_nom_table_tarif[0]
    elif(False):
        nom_table_tarif : str  = tab_nom_table_tarif[1]
    elif(False):
        nom_table_tarif : str  = tab_nom_table_tarif[2]

    print("quantite : " + str(quantite))
    print("prix : " + str(prix))
    print("indice : " + str(indice))

    # Trouvé ? : Modification sinon Insertion
    if(indice != -1):

        modification_tarif(commentaires, indice, nom_table_tarif, quantite, prix)
        return

    #requete insert stock
    tuple_valeurs = (partenaire_vendeur_id, vin_id, format_id, conditionnement_id, commentaires)

    requete = f"""INSERT INTO stock
    (partenaire_vendeur_id, vin_id, format_id, conditionnement_id, commentaires) VALUES (%s, %s, %s, %s, %s);"""

    req.envoie_requete_sans_retour2(requete, tuple_valeurs)

    print("insertion stock OK")

    #requete insert tarif
    tuple_valeurs = (quantite, prix)

    requete = f"""INSERT INTO """ + nom_table_tarif + """
    (quantite, prix) VALUES (%s, %s);"""

    req.envoie_requete_sans_retour2(requete, tuple_valeurs)                                                                                                    

    print("insertion tarif OK")

    for nom_table in tab_nom_table_tarif:

        if(nom_table != nom_table_tarif):

            #requete insert autres tarifs
            tuple_valeurs = (0, 0)

            requete = f"""INSERT INTO """ + nom_table + """(quantite, prix) VALUES (%s, %s);"""

            req.envoie_requete_sans_retour2(requete, tuple_valeurs)

    print("insertion autres tarifs OK")

    #requete récupération de l'indice
    requete = f"""SELECT MAX(id) FROM stock;"""

    indice_derniere_offre : int = req.envoie_requete_avec_retour(requete)[0][0]

    print("indice_derniere_offre : " + str(indice_derniere_offre))

    #requete insert stock_tarif
    tuple_valeurs = (indice_derniere_offre, indice_derniere_offre, indice_derniere_offre, indice_derniere_offre)

    requete = f"""INSERT INTO stock_tarifs(stock_id, tarif_officiel_stock_id, tarif_officieux_stock_id, tarif_export_stock_id) 
    VALUES (%s,%s,%s,%s);"""

    req.envoie_requete_sans_retour2(requete, tuple_valeurs)


    # Test et modification partenaire -> pays et type_parteanaire
    # Attention il faut tester que stock_tarifs soit bien rentrée

    # 5 Suppression des tarifs ayant les mêmes conditions que les offres rentrées en base et étant plus ancienne de deux jours (on évite le problème de tourner à une heure tardive)
    # Mettre une couleur sur les tarifs qui dépasse un certain délais (exemple orange : pour attention)

    # #Récupérer une date ancienne de deux jours
    # date_modification = datetime.today()
    # print("date_modification : "+date_modification)

    # date_modification_mois_deux_jours = date_modification - timedelta(2)
    # print("date_modification_mois_deux_jours : "+date_modification_mois_deux_jours)

    # requetes.suppression_offre(db, nom_negociant, vin, millesime, formatB, conditionnement, date_modification_mois_deux_jours)




