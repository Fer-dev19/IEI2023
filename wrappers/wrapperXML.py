import xml.etree.ElementTree as ET
import json

def xml_to_json(xml_file, json_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    data = []

    for row_elem in root.findall('.//row'):
        centro = {}
        for child_elem in row_elem:
            centro[child_elem.tag] = child_elem.text
        data.append(centro)
    
    if data and "row" in data[0] and data[0]["row"].strip() == "":
        data.pop(0)

    json_data = json.dumps(data, indent=2, ensure_ascii=False)

    with open(json_file, 'w', encoding='utf-8') as f:
        f.write(json_data)

xml_to_json('../archivosEntrada/CAT.xml', '../archivosJSON/CAT.json')
