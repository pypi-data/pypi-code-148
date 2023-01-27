def Astronaut_Tracker():
	#import json
	import urllib.request
	import turtle
	import json

	url = 'http://api.open-notify.org/astros.json'
	response = urllib.request.urlopen(url)
	astros = json.loads(response.read())

	print('People in Space: ', astros['number'])

	people = astros['people']

	for p in people:
  		print(p['name'], ' in ', p['craft'])
