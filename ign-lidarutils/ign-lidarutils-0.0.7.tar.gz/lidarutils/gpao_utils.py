""" fonctions utiles sur la gestion des gpao """

import json


class Job:
    """classe représentant un job"""

    def __init__(self, name, cmd):
        """constructeur"""

        """nom du job"""
        self.name = name
        """commande associée au job"""
        self.cmd = cmd

    def to_json(self):
        """conversion en json"""
        return {"name": self.name, "command": self.cmd}


class Lot:
    """classe représentant un lot"""

    def __init__(self, name, jobs=None, deps=None):
        """constructeur"""

        """nom du lot"""
        self.name = name
        """jobs du lot"""
        self.jobs = jobs
        """dépendances du lot"""
        self.deps = deps


        if not isinstance(self.jobs, list):
            self.jobs = []

        if not isinstance(self.deps, list):
            self.deps = []

    def to_json(self):
        """conversion en json"""
        json_elem = {"name": self.name}
        json_elem["jobs"] = []
        for job in self.jobs:
            json_elem["jobs"].append(job.to_json())
        if len(self.deps) > 0:
            json_elem["deps"] = []
            for dep in self.deps:
                json_elem["deps"].append({"id":dep})
        return json_elem


class BuilderGPAO:
    """classe permettant la construction d'un json de GPAO"""

    def __init__(self):
        """constructeur"""

        """liste des lots"""
        self.lots = []

    def add_lot(self, lot):
        """ajout d'un lot"""
        self.lots.append(lot)

    def save_as_json(self, file_json):
        """ecriture de la structure en json"""
        json_gpao = {"projects": []}
        for lot in self.lots:
            json_gpao["projects"].append(lot.to_json())
        with open(file_json, "w") as fjson:
            json.dump(json_gpao, fjson, indent=4)
