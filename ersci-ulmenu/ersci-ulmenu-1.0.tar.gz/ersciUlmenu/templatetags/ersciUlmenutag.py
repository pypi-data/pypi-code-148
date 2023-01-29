from django import template
from ..ersciUlmenu import UlMenuClass

register = template.Library()

@register.simple_tag
def ulmenu(model,parent_id):
	cl = UlMenuClass()
	clmenu = cl.ulmenu(model,parent_id)
	return  clmenu