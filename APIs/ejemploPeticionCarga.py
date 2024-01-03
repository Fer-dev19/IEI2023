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
