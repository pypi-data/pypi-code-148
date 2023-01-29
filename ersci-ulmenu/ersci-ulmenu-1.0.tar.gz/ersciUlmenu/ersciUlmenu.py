from django.utils.html import format_html
class UlMenuClass():
	txt = ""
	def __init__(self):
		txt = ""
	def ulmenu(self,model,parent_id):
		try:		
			model_query=model.filter(parent_id=parent_id)
			length=len(model_query)
			if length == 0:
				return
			else:
				self.txt += "<ul>"
			for i in range(length):				
				self.txt += "<li class='{}'>".format(model_query[i].css_class)	
				if model_query[i].link is not None and model_query[i].link != "":
					self.txt += "<a href='{}'>".format(model_query[i].link)
				self.txt += model_query[i].title
				if model_query[i].link is not None and model_query[i].link != "":
					self.txt += "</a>"
				self.ulmenu(model,model_query[i].id)
				self.txt += "</li>"
			self.txt += "</ul>"
			return format_html(self.txt)
		except:
			return "Error in your model or data!"
		

'''
from django.db import models

class Ulmenu(models.Model):
	title = models.CharField(max_length=100)
	css_class = models.CharField(max_length=100,null=True,blank=True)
	link = models.CharField(max_length=1000,null=True,blank=True)
	parent = models.ForeignKey("self", models.DO_NOTHING,null=True,blank=True,db_column='parent',related_name='children') 
	
	def __str__(self):
		return self.title
'''