import xml.etree.ElementTree as ET
import json

def xml_to_json(xml_file, json_file):
    # Parsear el archivo XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Crear una lista para almacenar los datos
    data = []

    # Recorrer los elementos del XML y extraer los datos
    for row_elem in root.findall('.//row'):
        centro = {}
        for child_elem in row_elem:
            # Utilizar el nombre del elemento como clave y el texto como valor
            centro[child_elem.tag] = child_elem.text

        # Agregar el diccionario a la lista de datos
        data.append(centro)
    
    # Excluir el primer elemento de la lista si es un salto de línea
    if data and "row" in data[0] and data[0]["row"].strip() == "":
        data.pop(0)

    # Convertir la lista de datos a formato JSON
    json_data = json.dumps(data, indent=2, ensure_ascii=False)

    # Escribir los datos en un archivo JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        f.write(json_data)

# Llamar a la función con el nombre del archivo XML y el nombre del archivo JSON
xml_to_json('../centres.xml', '../datos_xml_CAT.json')
