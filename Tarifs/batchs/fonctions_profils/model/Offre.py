class Offre:

    id_negociant : int
    vin : str
    millesime : str
    formatB : str
    prix : float
    quantite : int
    conditionnement : str
    commentaires : str 

    def __init__(self, id_negociant, tab_tarif_sans_id_negociant):
        print("Création de " + type(self).__name__);

        self.id_negociant = id_negociant
        self.vin = tab_tarif_sans_id_negociant[0]
        self.millesime = tab_tarif_sans_id_negociant[1]
        self.formatB = tab_tarif_sans_id_negociant[2]
        self.prix = tab_tarif_sans_id_negociant[3]
        self.quantite = tab_tarif_sans_id_negociant[4]
        self.conditionnement = tab_tarif_sans_id_negociant[5]
        self.commentaires = tab_tarif_sans_id_negociant[6]


    