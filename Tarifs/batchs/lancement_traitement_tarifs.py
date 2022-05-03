# from asyncio.windows_events import NULL
import sys
import os
from xmlrpc.client import boolean
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import traitement_tarifs as tt
# from traitement_tarifs import Traitement_Tarif

# php a enlevé // A changer
chemin_dossier_tarifs = "/var/www/html/projets/bureau-laurent-quancard/gestion-des-offres/gestion_tarifs_automatises/Tarifs/"

# A revoir utilité !! remplacer par 
dossier_sortie = "tarifs_HEBDO"

print("Hello lancement_traitement_tarifs")

# Simple lancement du traitment tarif pour éviter de relancer le traitement_tarif
# à cause d'un import d'une propriété générique
tt.traitement_tarif()

# traitement_tarif : Traitement_Tarif = Traitement_Tarif(chemin_dossier_tarifs, dossier_sortie)
# traitement_tarif.execution_traitement_tarif()


