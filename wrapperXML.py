import json
import xml.etree.ElementTree as ET

# Función para extraer datos desde un archivo XML
def extraer_datos_desde_xml(archivo_xml):
    try:
        tree = ET.parse(archivo_xml)
        root = tree.getroot()
        datos = []
        for row in root.findall('row'):
            dato = {}
            for child in row:
                if child.tag == 'row':
                    subdato = {}
                    for subchild in child:
                        subdato[subchild.tag] = subchild.text
                    datos.append(subdato)
                else:
                    dato[child.tag] = child.text
            datos.append(dato)
        return datos
    except FileNotFoundError:
        print(f"El archivo XML {archivo_xml} no se encontró.")
        return None
    except ET.ParseError as e:
        print(f"Error al analizar el archivo XML: {e}")
        return None
    
# Uso del wrapper para extraer datos de un XML
archivo_xml = './centres.xml'  # Reemplaza con la ubicación de tu archivo XML
datos_extraidos_xml = extraer_datos_desde_xml(archivo_xml)

# Guardar los datos del XML en un archivo JSON
archivo_json_xml = 'datos_xml_CAT.json'
try:
    with open(archivo_json_xml, 'w', encoding='utf-8') as archivo_json:
        json.dump(datos_extraidos_xml, archivo_json, ensure_ascii=False, indent=4)
    print(f"Los datos del XML se han guardado en {archivo_json_xml}.")
except Exception as e:
    print(f"Ocurrió un error al escribir los datos del XML en el archivo JSON: {e}")