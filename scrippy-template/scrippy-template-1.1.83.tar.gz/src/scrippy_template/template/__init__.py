#!/usr/bin/env python3
"""
Ce module permet la génération de document à partir de fichiers modèles.

Pour être utilisables les fichiers modèles devront être situés dans le répertoire "self.base_path".

Afin de gérer l'interpolation de variables le fichier modèle DOIT accepter un dictionnaire nommé "params" comme paramètre.

Ce dictionnaire devra contenir l'ensemble des variables nécessaires au rendu complet du fichier modèle.

Exemple:
--------

Avec le fichier modèle simple suivant:

"Bonjour {{params.user}}, ce mail vous est envoyé par {{params.sender}}."

Le dictionnaire "params" devra être:

params = {'user': 'harry.fink', 'sender': 'Luigi Vercotti'}
"""
import logging
import jinja2
from scrippy_template import ScrippyTemplateError


class Renderer:
  """L'objet Renderer est en charge du chargement et du rendu des fichiers modèles."""

  def __init__(self, base_path, template_filename):
    """
    L'instanciation d'un objet Renderer nécessite le nom du fichier modèle à charger.

    Le fichier modèle sera automatiquement récupéré dans le répertoire "self.base_path" et ne doit donc pas
    être un chemin absolu mais simplement un le nom du fichier en lui même.
    """
    self.base_path = base_path
    self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.base_path), autoescape=True)
    self.load(base_path, template_filename)

  def load(self, base_path, template_filename):
    """
    Permet à un même objet Renderer de charger un autre fichier modèle.

    Le fichier modèle précédemment chargé est perdu au chargement du nouveau fichier.
    """
    logging.info("[+] Chargement du modele")
    logging.info(f" '-> Modele: {base_path}/{template_filename}")
    self.template_filename = template_filename

  def render(self, params=None):
    """
    Renvoie le rendu du fichier modèle.

    Si des variables doivent être fournies au fichier modèle, elle doivent l'être sous la forme d'un
    dictionnaire.

    Le dictionnaire sera alors transmis au fichier modèle qui sera chargé de faire l'interpolation
    de ces variables.
    """
    logging.info("[+] Rendu du modele")
    try:

      template = self.env.get_template(self.template_filename)
      return template.render(params=params)
    except jinja2.exceptions.TemplateNotFound as err:
      err_msg = f"Modele introuvable: {self.template_filename}"
      raise ScrippyTemplateError(err_msg) from err
    except jinja2.exceptions.UndefinedError as err:
      err_msg = f"Erreur indefinie: [{err.__class__.__name__}] {err}"
      raise ScrippyTemplateError(err_msg) from err
    except Exception as err:
      logging.critical("Merci de remonter l'erreur suivante afin qu'elle soit integree au module scrippy_template")
      err_msg = f"Erreur inattendue: [{err.__class__.__name__}] {err}"
      raise ScrippyTemplateError(err_msg) from err
