import lxml.etree as etree
from lxml.etree import Element, SubElement, ElementTree


root = Element('Authors')
authors = ElementTree(root)

calderon = SubElement(root,'author', name='Calderón', cert= 'high')
name = SubElement(calderon, 'persName')
SubElement(name, 'forename').text = 'Pedro'
SubElement(name, 'surname', sort='1').text = 'Calderón'
SubElement(name, 'nameLink').text = 'de la'
SubElement(name, 'surname').text = 'Barca'
idno = SubElement(calderon, 'idno', type='wikidata').text = 'Q170800'
SubElement(calderon, 'idno', type='pnd').text = '118518399'

lope = SubElement(root,'author', name = 'Lope', cert='high')
name = SubElement(lope, 'persName')
SubElement(name, 'forename').text = 'Félix'
SubElement(name, 'surname', sort='1').text = 'Lope'
SubElement(name, 'nameLink').text = 'de'
SubElement(name, 'surname').text = 'Vega'
SubElement(name, 'surname').text = 'Carpio'
SubElement(lope, 'idno', type='wikidata').text = 'Q165257'

calderonatt = SubElement(root, 'author', cert='medium', name='Calderón')
name = SubElement(calderonatt, 'persName')
SubElement(name, 'forename').text = 'Pedro'
SubElement(name, 'surname', sort='1').text = 'Calderón'
SubElement(name, 'nameLink').text = 'de la'
SubElement(name, 'surname').text = 'Barca'
name.text = '(attr.)'
SubElement(calderonatt, 'idno', type='wikidata').text = 'Q170800'
SubElement(calderonatt, 'idno', type='pnd').text = '118518399'

lopeatt = SubElement(root, 'author', cert='medium', name='Lope')
name = SubElement(lopeatt, 'persName')
SubElement(name, 'forename').text = 'Félix'
SubElement(name, 'surname', sort='1').text = 'Lope'
SubElement(name, 'nameLink').text = 'de'
SubElement(name, 'surname').text = 'Vega'
SubElement(name, 'surname').text = 'Carpio'
name.text = '(attr.)'
SubElement(lopeatt, 'idno', type='wikidata').text = 'Q165257'

moreto = SubElement(root,'author', name='Moreto', cert='high')
name = SubElement(moreto, 'persName')
SubElement(name, 'forename').text = 'Agustín'
SubElement(name, 'surname').text = 'Moreto'
SubElement(moreto, 'idno', type='wikidata').text = 'Q399346'

moretoatt = SubElement(root,'author', cert='medium', name='Moreto')
name = SubElement(moretoatt, 'persName')
SubElement(name, 'forename').text = 'Agustín'
SubElement(name, 'surname').text = 'Moreto'
name.text = '(attr.)'
SubElement(moretoatt, 'idno', type ='wikidata').text = 'Q399346'

print(etree.tostring(authors))
authors.write("pretty.xml", encoding='UTF-8', pretty_print=True)
