# from extractores.extractorCV import ExtractorCV
# from wrappers import wrapperCSV, wrapperXML

# wrapperCSV.convertir_csv_a_json()
# extractor = ExtractorCV('./baseDatos.db', './archivosJSON/CV.json')
# extractor.ejecutar()

import requests

url = 'http://localhost:5003/cargar_datos'  # Reemplaza con la URL correcta de tu API
data = {
    'seleccion': ['Valencia']  # Ajusta esta lista según las comunidades que quieras cargar
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Respuesta de la API:", response.json())
else:
    print("Error al realizar la petición:", response.status_code, response.text)