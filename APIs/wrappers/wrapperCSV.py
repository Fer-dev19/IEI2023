import csv
import json

def convertir_csv_a_json():
    archivo_csv = './archivosEntrada/CV.csv'
    archivo_json_salida = './archivosJSON/CV.json'
    try:
        with open(archivo_csv, 'r', encoding='utf-8', newline='') as archivo:
            lector_csv = csv.DictReader(archivo, delimiter=';')
            datos = list(lector_csv)

        with open(archivo_json_salida, 'w', encoding='utf-8') as archivo_json:
            json.dump(datos, archivo_json, ensure_ascii=False, indent=4)

    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo CSV {archivo_csv} no se encontró.")
    except Exception as e:
        raise Exception(f"Ocurrió un error al convertir CSV a JSON: {e}")