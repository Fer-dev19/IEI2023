import csv
import json
import xml.etree.ElementTree as ET

# Función para extraer datos desde un archivo CSV
def extraer_datos_desde_csv(archivo_csv):
    datos = []
    try:
        with open(archivo_csv, 'r', encoding='utf-8', newline='') as archivo:
            lector_csv = csv.DictReader(archivo, delimiter=';')
            for fila in lector_csv:
                datos.append(fila)
        return datos
    except FileNotFoundError:
        print(f"El archivo CSV {archivo_csv} no se encontró.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al extraer datos del CSV: {e}")
        return None

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

# Uso del wrapper para extraer datos de un CSV
archivo_csv = './centrosValencia.csv'  # Reemplaza con la ubicación de tu archivo CSV
datos_extraidos_csv = extraer_datos_desde_csv(archivo_csv)

# Uso del wrapper para extraer datos de un XML
archivo_xml = './centres.xml'  # Reemplaza con la ubicación de tu archivo XML
datos_extraidos_xml = extraer_datos_desde_xml(archivo_xml)

# Guardar los datos del CSV en un archivo JSON
archivo_json_csv = 'datos_csv_CV.json'
try:
    with open(archivo_json_csv, 'w', encoding='utf-8') as archivo_json:
        json.dump(datos_extraidos_csv, archivo_json, ensure_ascii=False, indent=4)
    print(f"Los datos del CSV se han guardado en {archivo_json_csv}.")
except Exception as e:
    print(f"Ocurrió un error al escribir los datos del CSV en el archivo JSON: {e}")

# Guardar los datos del XML en un archivo JSON
archivo_json_xml = 'datos_xml_CAT.json'
try:
    with open(archivo_json_xml, 'w', encoding='utf-8') as archivo_json:
        json.dump(datos_extraidos_xml, archivo_json, ensure_ascii=False, indent=4)
    print(f"Los datos del XML se han guardado en {archivo_json_xml}.")
except Exception as e:
    print(f"Ocurrió un error al escribir los datos del XML en el archivo JSON: {e}")
