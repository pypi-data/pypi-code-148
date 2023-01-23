"""  Application d'un (ou plusieurs) filtre(s) PDAL """

import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass

from lidarutils import file_utils

"""
    Exemple d'utilisation :
    
    pipeline = []
    pipeline.append(PdalReader("toto.las")
    pipeline.append(PdalFilter("info", [["where", "Classification==0"]]))
    pipeline.append(PdalWriter("export.ply")

    #Le pipeline est écrit dans fic_pipeline_json. 
    #Le nom de ce fichier doit se terminer par "_pipeline.json". 
    #Si le nom ne se termine pas comme cela (par ex on a mis le fichier las concerné), 
    #on remplace las par le bon suffixe.
    pdal_pipeline.run_pdal_elements(pipeline, fic_pipeline_json, fic_metadata_out)

"""

##########################################################################


def find_pdal_exe():
    """recherche de l'exe pdal"""
    pdal_name = "pdal"
    if sys.platform.startswith("win32"):
        pdal_name += ".exe"
    return file_utils.find_program(pdal_name)


##########################################################################


@dataclass
class PdalElement:
    """Paramètres d'un élément pdal"""

    def __init__(self, atype, name, options=None):
        """type d'action (readers, writers ou filters)"""
        assert atype in ["readers", "writers", "filters"]
        self.type = atype
        """nom du traitement ou format I/O"""
        self.name = name
        """options liées au traitement/format choisi"""
        if isinstance(options, list):
            for option in options:
                if option[0] == "filename":
                    # gestion des chemins windows
                    if sys.platform.startswith("win32"):
                        option[1] = option[1].replace("\\", "/")
            self.options = options
        else:
            self.options = []


##########################################################################


@dataclass
class PdalFilter(PdalElement):
    """Filter simple"""

    def __init__(self, name, options=None):
        super().__init__("filters", name, options)


##########################################################################


def get_driver_from_ext(ext_file):
    """renvoie le driver associé à l'extension du fichier"""
    m_exts_driver = [
        ["las", ["las", "laz"]],
        ["org", ["geojson"]],
        ["gdal", ["tif", "tiff", "bil", "png"]],
        ["ply", ["ply"]],
        ["text", ["txt"]],
        ["gltf", ["glb"]],
    ]  # a completer au besoin
    for m_ext in m_exts_driver:
        for ext in m_ext[1]:
            if ext_file == ext:
                return m_ext[0]
    raise Exception("Aucun driver pdal trouvé")


@dataclass
class PdalIO(PdalElement):
    """IO"""

    def __init__(self, name, options=None):
        """constructeur"""

        # options d'export/import
        self.options = options

        if not isinstance(options, list):
            self.options = []
        self.options.append(["filename", name])

        _, ext = os.path.splitext(name)
        super().__init__(self._type_io, get_driver_from_ext(ext[1:]), self.options)


@dataclass
class PdalReader(PdalIO):
    """Reader simple"""

    def __init__(self, name, options=None):
        self._type_io = "readers"
        super().__init__(name, options)


@dataclass
class PdalWriter(PdalIO):
    """Writer simple"""

    def __init__(self, name, options=None):
        self._type_io = "writers"
        super().__init__(name, options)


##########################################################################


def pdal_element(elem):
    """Element de traitement pdal"""

    # options est un tableau de pair d'options (ex : [where,condition] )
    # a l'utilisateur de mettre les bonnes options (cf. doc pdal)
    json_elem = {"type": elem.type + "." + elem.name}
    for option in elem.options:
        json_elem[option[0]] = option[1]

    return json_elem


##########################################################################


def create_pipeline_name(base):
    """Creation d'un nom de fichier pour un pipeline json à partir d'un autre fichier (las par ex)"""
    # _, file_extension = os.path.splitext(base)
    # return base.replace(file_extension, "_pipeline.json")
    return os.path.basename(base) + "_pipeline.json"


##########################################################################


def write_pipeline(element_list, fic_pipe):
    """Ecriture d'un pipeline avec plusieurs éléments PDAL"""

    # ajout des éléments du pipeline
    json_pipe = {"pipeline": []}
    for element in element_list:
        json_pipe["pipeline"].append(pdal_element(element))

    # Ecriture du json
    with open(fic_pipe, "w") as outfile:
        json.dump(json_pipe, outfile, indent=4)


##########################################################################


class PipelineFailedError(Exception):
    """Exception lors du lancement de la commande pdal"""

    def __init__(self, command):
        super().__init__("la commande " + command + " a échouée : " + str(Exception))


##########################################################################


def run_subprocess(commande):
    """Lancement d'un subprocess"""

    try:
        subprocess.run(
            commande,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            check=True,
        )
    except subprocess.CalledProcessError:
        raise PipelineFailedError(commande)
    except subprocess.PermissionError:
        raise PipelineFailedError(commande)

def run_pdal_pipeline(fic_pipe, fic_stats=None):
    """Lancement d'un pipeline"""

    pdal_exe = find_pdal_exe()
    if pdal_exe is None:
        raise Exception("Pdal non trouvé")

    # suppression du ficStats si déjà existant
    if fic_stats is not None and os.path.exists(fic_stats):
        os.remove(fic_stats)

    # application de la commande
    commande = pdal_exe + " pipeline " + fic_pipe
    if fic_stats is not None:
        commande += " --metadata " + fic_stats

    run_subprocess(commande)

def run_pdal_info(fic_las, fic_stats):
    """Lancement d'un pdal info"""

    pdal_exe = find_pdal_exe()
    if pdal_exe is None:
        raise Exception("Pdal non trouvé")

    # suppression du ficStats si déjà existant
    if os.path.exists(fic_stats):
        os.remove(fic_stats)

    # application de la commande
    commande = pdal_exe + " info " + fic_las + " --metadata > " + fic_stats

    run_subprocess(commande)


def run_pdal_elements(element_list, fic_stats=None):
    """Ecriture d'un pipeline PDAL et lancement"""
    fic_pipe = tempfile.NamedTemporaryFile(suffix="_pipeline.json")
    fic_pipe.close()
    write_pipeline(element_list, fic_pipe.name)
    run_pdal_pipeline(fic_pipe.name, fic_stats)
    os.remove(fic_pipe.name)
