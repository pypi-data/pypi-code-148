from django.template.loader import render_to_string
from django.conf import settings


def generar_addenda(diccionario):
    return render_to_string("cfdi/addendas/zobele.xml", diccionario)
