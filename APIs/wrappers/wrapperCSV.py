import csv
import json

#Con esté único método utilizamos la libreria de csv de python para poder transformar
#el archivo csv a json para posteriormente, en los extractores extraer los datos
#y utilizarlos para insertarlos
def convertir_csv_a_json():
    archivo_csv = './archivosEntrada/CV.csv'
    archivo_json_salida = './archivosJSON/CV.json'
    try:
        #Arbimos el archivo
        with open(archivo_csv, 'r', encoding='utf-8', newline='') as archivo:
            lector_csv = csv.DictReader(archivo, delimiter=';')
            #Pasamos los datos a la variable datos
            datos = list(lector_csv)

        #Vertemos los datos en el archivo json de salida
        with open(archivo_json_salida, 'w', encoding='utf-8') as archivo_json:
            json.dump(datos, archivo_json, ensure_ascii=False, indent=4)

    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo CSV {archivo_csv} no se encontró.")
    except Exception as e:
        raise Exception(f"Ocurrió un error al convertir CSV a JSON: {e}")