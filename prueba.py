import json
with open('./datos_xml_CAT.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    for entry in data: 
        print(entry['codi_postal'])