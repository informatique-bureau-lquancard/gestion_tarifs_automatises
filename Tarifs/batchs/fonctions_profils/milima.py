# MILIMA
def fct_flux_tree_xml_1(flux, chemin_fichier_sortie, nom_tarif_profil, id_negociant):

    print ("  fct_flux_tree  ")

    print(flux)

    # ??? normalement il y a déjà flux en haut, supprimer et remplacer par flux ? voir par rapport à la base
    type_flux = "flux_xml"

    # Ce n'est pas bon à changer 
    type_tarif_id = 1

    print("flux : ")
    print(flux)

    tree = etree.parse(flux)

    Vin = etree.Element("Produit")

    # Suppression des données d'un client avant de rajouter les offres de ce client
    pb.req.supprimer_tout_par_id_stock_offres(id_negociant)
    pb.req.supprimer_tout_par_partenaire(id_negociant)

    with open(chemin_fichier_sortie,'w',newline='', encoding='utf-8') as monFichierSortie:
        writer = csv.writer(monFichierSortie, delimiter=';', quoting=csv.QUOTE_NONE, escapechar=';', quotechar='')

        taille : int = len( tree.xpath("/XMLFILE") )

        print("taille : " + str(taille) )

        taille : int = len( tree.xpath("/XMLFILE/Produit") )

        print("taille : " + str(taille) )

        for Vin in tree.xpath("/XMLFILE/Produit") :

            # couleur
            couleur : str = (Vin[4].text).upper()

            # vin, enlève la date de vin
            vin : str = unidecode((Vin[0].text)[:-5])

            vin = ft.formaterVin("", vin, couleur)

            # millesime
            millesime : str = ft.formaterAnnee( Vin[1].text )

            # formatB
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

            # insertion des lignes dans le fichier
            newRow=[vin,millesime,formatB,prix,quantite,conditionnement,commentaires]

            # insertion des lignes dans la base
            pb.insertion_tarif(type_tarif_id, nom_tarif_profil,vin,millesime,formatB,prix,quantite,conditionnement,commentaires, id_negociant)

            writer.writerow(newRow)
        return writer