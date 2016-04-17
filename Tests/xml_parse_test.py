from bs4 import BeautifulSoup

xml_data = open("test.xml").read()
parsed_xml = BeautifulSoup(xml_data, 'html.parser')
ids = parsed_xml.findAll("release")

for id in ids:
    print(id["id"])