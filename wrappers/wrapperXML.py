import xml.etree.ElementTree as ET
import json

import xml.etree.ElementTree as ET
import json

def convertir_xml_a_json(archivo_xml, archivo_json_salida):
    """
    Lee un archivo XML y lo convierte en un archivo JSON.

    Args:
    archivo_xml (str): Ruta al archivo XML de entrada.
    archivo_json_salida (str): Ruta al archivo JSON de salida.
    """
    try:
        tree = ET.parse(archivo_xml)
        root = tree.getroot()

        data = []
        for row_elem in root.findall('.//row'):
            centro = {child_elem.tag: child_elem.text for child_elem in row_elem}
            data.append(centro)

        if data and "row" in data[0] and data[0]["row"].strip() == "":
            data.pop(0)

        with open(archivo_json_salida, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    except ET.ParseError:
        raise ValueError(f"Error al analizar el archivo XML: {archivo_xml}")
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo XML {archivo_xml} no se encontró.")
    except Exception as e:
        raise Exception(f"Ocurrió un error al convertir XML a JSON: {e}")

# Ejemplo de uso
try:
    convertir_xml_a_json('../archivosEntrada/CAT.xml', '../archivosJSON/CAT.json')
    print("Conversión completada con éxito.")
except Exception as e:
    print(e)


# def xml_to_json(xml_file, json_file):
#     tree = ET.parse(xml_file)
#     root = tree.getroot()

#     data = []

#     for row_elem in root.findall('.//row'):
#         centro = {}
#         for child_elem in row_elem:
#             centro[child_elem.tag] = child_elem.text
#         data.append(centro)
    
#     if data and "row" in data[0] and data[0]["row"].strip() == "":
#         data.pop(0)

#     json_data = json.dumps(data, indent=2, ensure_ascii=False)

#     with open(json_file, 'w', encoding='utf-8') as f:
#         f.write(json_data)

# xml_to_json('../archivosEntrada/CAT.xml', '../archivosJSON/CAT.json')
