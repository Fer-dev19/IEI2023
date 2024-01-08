import xml.etree.ElementTree as ET
import json

#Con esté único método utilizamos la libreria de xml de python para poder transformar
#el archivo xml a json para posteriormente, en los extractores extraer los datos
#y utilizarlos para insertarlos
def convertir_xml_a_json():
    #Rutas de los archivos de entrada y salida
    archivo_xml = './archivosEntrada/CAT.xml'
    archivo_json_salida = './archivosJSON/CAT.json'
    try:
        #Parseamos el archivo xml y obtenemos su raíz 
        tree = ET.parse(archivo_xml)
        root = tree.getroot()
        #Inicializamos una lista para almacenar los datos covertidos
        data = []
        #Iteramos sobre cada elemento 'row' en el XML
        for row_elem in root.findall('.//row'):
        #Creamos un diccionario para cada 'row', con tags como claves y textos como valores.
            centro = {child_elem.tag: child_elem.text for child_elem in row_elem}
            data.append(centro)

        #Aquí comprobamos si el primer elemento es vacío y de serlo lo eliminamos
        if data and "row" in data[0] and data[0]["row"].strip() == "":
            data.pop(0)

        #Crea el archivo json y vierte los datos convertidos
        with open(archivo_json_salida, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    except ET.ParseError:
        raise ValueError(f"Error al analizar el archivo XML: {archivo_xml}")
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo XML {archivo_xml} no se encontró.")
    except Exception as e:
        raise Exception(f"Ocurrió un error al convertir XML a JSON: {e}")
