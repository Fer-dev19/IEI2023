import xml.etree.ElementTree as ET
import json

def convertir_xml_a_json():
    archivo_xml = './archivosEntrada/CAT.xml'
    archivo_json_salida = './archivosJSON/CAT.json'
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
