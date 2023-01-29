from django.shortcuts import render
from .models import Ulmenu
from .ersciUlmenu import UlMenuClass
# Create your views here.

def index(request):
	model=Ulmenu.objects.all()
	cl = UlMenuClass()
	clmenu = cl.ulmenu(Ulmenu.objects.all(),None)
	return render(request,"ersciUlmenutemp/index.html",{'data' : clmenu , 'model' : model })