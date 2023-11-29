import csv
import json

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

archivo_csv = '../archivosEntrada/CV.csv'
datos_extraidos_csv = extraer_datos_desde_csv(archivo_csv)

archivo_json_csv = '../archivosJSON/CV.json'
try:
    with open(archivo_json_csv, 'w', encoding='utf-8') as archivo_json:
        json.dump(datos_extraidos_csv, archivo_json, ensure_ascii=False, indent=4)
    print(f"Los datos del CSV se han guardado en {archivo_json_csv}.")
except Exception as e:
    print(f"Ocurrió un error al escribir los datos del CSV en el archivo JSON: {e}")