""" fonctions utiles a propos de conda """
import os
import tempfile

##########################################################################

CONDA_PATH = None

def get_conda_active_path():
    """retourne le chemin conda actif"""

    global CONDA_PATH

    if CONDA_PATH is not None:
        return CONDA_PATH

    fic_tmp = tempfile.NamedTemporaryFile(suffix="_get_conda_active_path")
    fic_tmp.close()

    commande = "conda info > " + fic_tmp.name
    os.system(commande)

    if not os.path.exists(fic_tmp.name):
        print("Pb dans le lancement de 'conda info'")
        return None

    fin = open(fic_tmp.name, "r")

    for line in fin:
        if line.find("active env location") >= 0:
            mots = line.split(" : ")
            CONDA_PATH = mots[1].rstrip()
            break

    fin.close()
    os.remove(fic_tmp.name)

    return CONDA_PATH
