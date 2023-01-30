from django.db import models

class Ulmenu(models.Model):
	title = models.CharField(max_length=100)
	css_class = models.CharField(max_length=100,null=True,blank=True)
	link = models.CharField(max_length=1000,null=True,blank=True)
	parent = models.ForeignKey("self", models.DO_NOTHING,null=True,blank=True) 
	
	def __str__(self):
		return self.title
