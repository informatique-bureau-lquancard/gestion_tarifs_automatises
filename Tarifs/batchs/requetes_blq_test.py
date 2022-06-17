# Marche

from numpy import deprecate_with_doc
import mysql.connector

# from mysql import connector

#####--------------------------MISE EN PLACE DE LA CONNEXION ET REQUETES BASIQUES--------------------------#####

machine = "localhost"
# machine = "192.168.100.178"
utilisateur = "root"
password_ssh = "Be8aichei3xungoh"
base_donnee = "bd_blq"

connection_base_bd_blq : mysql.connector.connection.MySQLConnection = mysql.connector.connect(host = machine, user = utilisateur, password = password_ssh, database = base_donnee)

def envoie_requete_avec_retour(requete : str):
    
    curseur : mysql.connector.cursor.MySQLCursor = connection_base_bd_blq.cursor()

    curseur.execute(requete)

    sortie_requete : list = list(map(list, curseur.fetchall()))

    # print("sortie_requete")
    # print(sortie_requete)

    curseur.close()
    # print("sortie_requete : ")
    # print(sortie_requete)

    if(len(sortie_requete) > 0):
        return sortie_requete

    return [[-1]]

def envoie_requete_sans_retour(requete : str):
    curseur = connection_base_bd_blq.cursor()

    curseur.execute(requete)

    # sortie_requete = list(map(list, curseur.fetchall()))

    connection_base_bd_blq.commit()

    curseur.close()

def envoie_requete_tuple_avec_retour(requete : str, tab_valeurs : tuple):
    
    curseur : mysql.connector.cursor.MySQLCursor = connection_base_bd_blq.cursor()

    curseur.execute(requete, tab_valeurs)

    sortie_requete : list = list(map(list, curseur.fetchall()))

    curseur.close()
    # print("sortie_requete : ")
    # print(sortie_requete)

    if(len(sortie_requete) > 0):
        print("sortie_requete : " + str(sortie_requete))
        return sortie_requete

    return [[-1]]

def envoie_requete_tuple_sans_retour(requete : str, tab_valeurs : tuple):
    curseur = connection_base_bd_blq.cursor()

    curseur.execute(requete, tab_valeurs)

    # sortie_requete = list(map(list, curseur.fetchall()))

    connection_base_bd_blq.commit()

    curseur.close()

#####--------------------------REQUETES DE RECUPERATION--------------------------#####

def compte_nombre_doublon( liste_designation : list, tuple_valeurs : tuple ):

    liste_designation : str

    nom_table : str = liste_designation[0]
    designations_colonne : list = liste_designation[1:]

    requete : str = f"""SELECT count(*) FROM """ + nom_table + """ WHERE """ 

    partie_requete : str = ""
    indice : int = 0

    for designation in designations_colonne :
        
        if( indice != 0 ):
            partie_requete += """ AND """

        partie_requete += designation + """ = %s"""

        indice = indice + 1

    requete = requete + partie_requete + """;"""

    return envoie_requete_tuple_avec_retour(requete, tuple_valeurs)[0][0]

def recuperation_tab(nom_table: str): 

    requete : str = f"SELECT * FROM `{nom_table}`;"

    table_apres_requete = envoie_requete_avec_retour(requete)

    # print("ok")
    # print(table_apres_requete)

    return table_apres_requete;

def recuperation_profils_negociants():
    requete : str = f"""SELECT pr.profil, pr.chemin, pr.flux, tp.type_tarif, tp.description, f.nom, f.type, p.id FROM `profil` as pr
                        JOIN `type_tarif` as tp ON pr.type_tarif_id = tp.id
                        JOIN `flux` as f ON pr.flux_id = f.id
                        JOIN `partenaire` as p ON pr.partenaire_id = p.id;"""

    curseur = connection_base_bd_blq.cursor()

    curseur.execute(requete)

    sortie_requete = list(map(list, curseur.fetchall()))

    curseur.close()

    # print(sortie_requete)

    return sortie_requete

# A changer !!!
# méthode qui sert qu'à un seul endroit, méthode au dessous qui fait presque pareil, nom a changer !!! 
def recuperation_indice_doublon(nom_table :str, nom_colonne : str, valeur_a_testee : str):

    # print("nom_table : -"+ nom_table+"-")
    # print("nom_colonne : -"+ nom_colonne+"-")
    # print("valeur_a_testee : -"+ valeur_a_testee+"-")

    valeur_a_testee = valeur_a_testee.replace("'","")

    if(valeur_a_testee.isdigit()):
        requete : str = f"""SELECT id FROM """ + nom_table + """ WHERE """ + nom_colonne + """ = """ + valeur_a_testee + """ HAVING (COUNT(*) > 0);"""
    else:
        requete : str = f"""SELECT id FROM """ + nom_table + """ WHERE """ + nom_colonne + """ = '""" + valeur_a_testee + """' HAVING (COUNT(*) > 0);"""  

    return envoie_requete_avec_retour(requete)[0][0]



def recuperation_un_element(nom_table :str, nom_colonne : str, valeur_a_testee : str, valeur_a_recuperee : str):

    # print("nom_table : -"+ nom_table+"-")
    # print("nom_colonne : -"+ nom_colonne+"-")
    # print("valeur_a_testee : -"+ valeur_a_testee+"-")

    valeur_a_testee = valeur_a_testee.replace("'","")

    if(valeur_a_testee.isdigit()):
        requete : str = f"""SELECT """ + valeur_a_recuperee + """ FROM """ + nom_table + """ WHERE """ + nom_colonne + """ = """ + valeur_a_testee + """;"""
    else:
        requete : str = f"""SELECT """ + valeur_a_recuperee + """ FROM """ + nom_table + """ WHERE """ + nom_colonne + """ = '""" + valeur_a_testee + """';"""

    return envoie_requete_avec_retour(requete)[0][0]

def recuperation_un_id(nom_table :str, nom_colonne : str, valeur_a_testee : str):
    
    # print("nom_table : -"+ nom_table+"-")
    # print("nom_colonne : -"+ nom_colonne+"-")
    # print("valeur_a_testee : -"+ valeur_a_testee+"-")

    valeur_a_testee = valeur_a_testee.replace("'","")

    if(valeur_a_testee.isdigit()):
        requete : str = f"""SELECT id FROM """ + nom_table + """ WHERE """ + nom_colonne + """ = """ + valeur_a_testee + """;"""
    else:
        requete : str = f"""SELECT id FROM """ + nom_table + """ WHERE """ + nom_colonne + """ = '""" + valeur_a_testee + """';"""

    return envoie_requete_avec_retour(requete)[0][0]

def recuperation_elements_proche(nom_table :str, nom_colonne : str, valeur_a_testee : str):

    valeur_a_testee = valeur_a_testee.replace("'","")

    requete : str = f"""SELECT id FROM """ + nom_table + """ WHERE """ + nom_colonne + """ = '%""" + valeur_a_testee + """%';"""

    resultat : list = list( envoie_requete_avec_retour(requete) )

    return resultat

#####--------------------------REQUETES DE SUPPRESSION--------------------------#####

def supprimer_tout(tab_table : list):

    for table in tab_table:
        requete = f"""DELETE FROM {table};"""

        envoie_requete_sans_retour(requete)

def supprimer_tout_par_partenaire(idNegociant : int):
    
    requete = f"""DELETE FROM stock_offres WHERE partenaire_vendeur_id = {idNegociant};"""

    envoie_requete_sans_retour(requete)

def supprimer_tout_par_id_stock_offres(idNegociant : int):
    
    requete = f"""DELETE FROM tarif 
                    WHERE stock_id IN (
	                    SELECT id FROM stock_offres WHERE partenaire_vendeur_id = {idNegociant}
                    );
    """

    # print("requete : " + requete)

    envoie_requete_sans_retour(requete)

#####--------------------------REQUETES INITIALISATION--------------------------#####

# Utilisé apres une suppression dans les données d'une table
def reinitialiser_auto_increment(tab_table):

    for table in tab_table:
        requete = f"""ALTER TABLE {table} AUTO_INCREMENT = 0;"""

        envoie_requete_sans_retour(requete)

def reinitialisation_global(tab_table : list):

    for table in tab_table:

        requete = f"""DELETE FROM {table};"""

        envoie_requete_sans_retour(requete)

        requete = f"""ALTER TABLE {table} AUTO_INCREMENT = 0;"""

        envoie_requete_sans_retour(requete)

#####--------------------------REQUETES INSERTION--------------------------#####

# Ne marche pas
@deprecate_with_doc
def insertion_simple(nom_table : str, champs : tuple, tab_valeurs : tuple):

    indice_champs : int = len(champs)

    # print(indice_champs)

    tab_valeurs : tuple = champs + tab_valeurs

    # print(tab_valeurs)

    chaine_str : str = f"""%s"""

    # print(chaine_str)

    if(indice_champs > 1):

        for i in range(1, indice_champs):
            chaine_str += f""", %s"""

            # print(chaine_str)

    requete : str = f"""INSERT INTO """+ nom_table +"""(""" + chaine_str + """) VALUES ("""+ chaine_str +""");"""

    # print(requete)

    envoie_requete_tuple_sans_retour(requete, tab_valeurs)



#A tester ou supprimer !!

# def requete_insertion_tarif(id, nom_table, quantite, prix, date, indice):
#     requete : str

#     requete = f"""INSERT INTO '{nom_table}'
#     (id, quantite, tarif, date_maj) VALUES ('{id}','{quantite}','{prix}', '{date}')
#     WHERE id = '{indice}'"""

#     return requete

# def requete_insertion_tarifs(id, quantite, prix, indice):
#     date = '2005-05-10'

#     tab_nom_tarif = ['tarif_officiel_stock', 'tarif_officieux_stock', 'tarif_export_stock']

#     #requete insert
#     # id, nom_table, quantite, prix, date, indice
#     requete = requete_insertion_tarif(id, 'tarif_officiel_stock', quantite, prix, date, indice)

#     traitement_tarifs.envoie_requete_sans_retour(requete)

#     # id, nom_table, quantite, prix, date, indice
#     requete = requete_insertion_tarif(id, 'tarif_officieux_stock', '0', '0', date, indice)

#     traitement_tarifs.envoie_requete_sans_retour(requete)

#     # id, nom_table, quantite, prix, date, indice
#     requete = requete_insertion_tarif(id, 'tarif_export_stock', '0', '0', date, indice)

#     traitement_tarifs.envoie_requete_sans_retour(requete)

# #####--------------------------INSERTION--------------------------#####

# # Insertion d'un utilisateur
# #Besoin de cette requête ???
# def insertion_utilisateur(db, nom, prenom, email):
#     requete =   f"""INSERT INTO 'utilisateur' ('nom', 'prenom', 'email')
#                     VALUES ('{nom}', '{prenom}', '{email}');"""
#     db.commit()

# #A revoir stock tarifs 

# # Insertion d'une source
# def insertion_source(db, nom):
#     requete =   f"""INSERT INTO 'source' ('nom')
#                     VALUES ('{nom}');"""
#     db.commit()

# # Insertion d'un conditionnement
# def insertion_conditionnement(db, conditionnement):
#     requete =   f"""INSERT INTO 'conditionnement' ('conditionnement')
#                     VALUES ('{conditionnement}');"""
#     db.commit()

# # Insertion d'un format_bouteille
# def insertion_format_bouteille(db, format_bouteille):
#     requete =   f"""INSERT INTO 'format_bouteille' ('format_bouteille')
#                     VALUES ('{format_bouteille}');"""
#     db.commit()

# # Insertion d'un millesime
# def insertion_millesime(db, annee):
#     requete =   f"""INSERT INTO 'millesime' ('annee')
#                     VALUES ('{annee}');"""
#     db.commit()

# # Insertion d'une appellation
# def insertion_appellation(db, appellation):
#     requete =   f"""INSERT INTO 'domaine' ('appellation')
#                     VALUES ('{appellation}');"""
#     db.commit()

# # Insertion d'un domaine
# def insertion_domaine(db, nom):
#     requete =   f"""INSERT INTO 'domaine' ('nom')
#                     VALUES ('{nom}');"""
#     db.commit()

# # Insertion d'une periode de vin
# def insertion_vin(db, nom, domaine_id, appellation_id):
#     requete =   f"""INSERT INTO 'vin' ('nom', 'domaine_id', 'appellation_id')
#                     VALUES ('{nom}', '{domaine_id}', '{appellation_id}');"""
#     db.commit()

# # Insertion d'une periode de vente
# def insertion_periode_vente(db, date_debut, date_fin, nom):
#     requete =   f"""INSERT INTO 'periode_vente' ('date_debut', 'date_fin', 'nom')
#                     VALUES ('{date_debut}', '{date_fin}', '{nom}');"""
#     db.commit()

# # Insertion d'une vente
# def insertion_vente_a_distributeur(db, partenaire_vendeur_id, partenaire_acheteur_id, vin_id, periode_vente_id, quantite_equivalent_75cl):
#     requete =   f"""INSERT INTO 'vente_a_distributeur' ('partenaire_vendeur_id', 'partenaire_acheteur_id', 'vin_id', 'periode_vente_id', 'quantite_equivalent_75cl')
#                     VALUES ('{partenaire_vendeur_id}', '{partenaire_acheteur_id}', '{vin_id}', '{periode_vente_id}', '{quantite_equivalent_75cl}');"""
#     db.commit()

# # Insertion d'un pays
# def insertion_pays(db, nom, continent):
#     requete =   f"""INSERT INTO 'pays' ('nom', 'continent')
#                     VALUES ('{nom}', '{continent}');"""
#     db.commit()

# # Insertion d'un type de partenaire
# def insertion_type_partenaire(db, type):
#     requete =   f"""INSERT INTO 'type_partenaire' ('type')
#                     VALUES ('{type}');"""
#     db.commit()

# # Insertion d'un partenaire
# # A revoir pour la date de mise à jour des données dans la base. Nécessité de mettre la date ??
# def insertion_partenaire(db, pays_id, type_id, nom, date_maj):
#     requete =   f"""INSERT INTO 'partenaire' ('pays_id', 'type_id', 'nom', 'date_maj')
#                     VALUES ('{pays_id}', '{type_id}', '{nom}', '{date_maj}');"""
#     db.commit()

# # Insertion d'une offre dans le stock d'un partenaire
# def insertion_offre(db, partenaire_vendeur, vin, millesime, formatB, conditionnement, source, commentaires):
#     requete =   f"""INSERT INTO 'stock' ('partenaire_vendeur_id', 'vin_id', 'millesime_id', 'format_id', 'conditionnement_id', 'source_id', 'commentaires')
#                     VALUES ('{partenaire_vendeur}', '{vin}', '{millesime}', '{formatB}', '{conditionnement}', '{source}', '{commentaires}');"""
#     db.commit()

# #####--------------------------SELECTION--------------------------#####

# # Selection d'une offre dans le stock d'un partenaire
# def selection_offre(db, curseur, partenaire_vendeur, vin, millesime, formatB, conditionnement, source, commentaires):
#     requete =   f"""SELECT 'partenaire_vendeur_id', 'vin_id', 'millesime_id', 'format_id', 'conditionnement_id', 'source_id', 'commentaires' FROM 'stock'
#                     WHERE   partenaire_vendeur_id = '{partenaire_vendeur}', 
#                             vin_id = '{vin}', 
#                             millesime_id = '{millesime}', 
#                             format_id = '{formatB}', 
#                             conditionnement_id = '{conditionnement}', 
#                             source_id = '{source}', 
#                             commentaire_id = '{commentaires}' ;"""
#     curseur.execute(requete)

#     return curseur.fetchall()

#     # db.commit()

# #####--------------------------TESTS--------------------------#####

# # Modification d'une offre dans le stock d'un partenaire
# def modification_offre(db, partenaire_vendeur, vin, millesime, formatB, conditionnement, source, commentaires):
#     requete =   f"""UPDATE 'stock'  SET partenaire_vendeur_id = '{partenaire_vendeur}', 
#                                         vin_id = '{vin}', 
#                                         millesime_id = '{millesime}',
#                                         format_id = '{formatB}',
#                                         conditionnement_id = '{conditionnement}',
#                                         source_id = '{source}', 
#                                         commentaire_id = '{commentaires}'
#                     WHERE   partenaire_vendeur_id = '{partenaire_vendeur}', 
#                             vin_id = '{vin}', 
#                             millesime_id = '{millesime}', 
#                             format_id = '{formatB}', 
#                             conditionnement_id = '{conditionnement}', 
#                             source_id = '{source}', 
#                             commentaire_id = '{commentaires}' ;"""
#     db.commit()

# #####--------------------------TESTS--------------------------#####

# # # Insertion d'une offre dans le stock d'un partenaire
# # def remplace_doublon(db, partenaire_vendeur_id, vin_id, millesime_id, format_id, conditionnement_id, source_id, commentaires):
# #     requete =   f"""CASE 
# #                         WHEN a>b THEN 'A supérieur à B'
# #                         ELSE 'A inférieur à B'
# #                     END"""
    
    
    
# #     INSERT INTO 'stock' ('partenaire_vendeur_id', 'vin_id', 'millesime_id', 'format_id', 'conditionnement_id', 'source_id', 'commentaires')
# #                     VALUES ('{partenaire_vendeur_id}', '{vin_id}', '{millesime_id}', '{format_id}', '{conditionnement_id}', '{source_id}', '{commentaires}')
# #     db.commit()

# #####--------------------------SUPPRESSION--------------------------#####

# # Suppression d'une offre dans le stock d'un partenaire
# def suppression_offre(db, partenaire_vendeur, vin, millesime, formatB, conditionnement, date_modification_mois_deux_jours):
#     requete =   f"""DELETE FROM 'stock'
#                     WHERE   partenaire_vendeur_id = '{partenaire_vendeur}', 
#                             vin_id = '{vin}', 
#                             millesime_id = '{millesime}', 
#                             format_id = '{formatB}', 
#                             conditionnement_id = '{conditionnement}', 
#                             source_id = '{date_modification_mois_deux_jours}';"""
#     db.commit()