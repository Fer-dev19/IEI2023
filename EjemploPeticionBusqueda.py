
import requests

url = 'http://127.0.0.1:5000/getCentros'
# Parámetros a pasar
response = requests.get(url)

if response.status_code == 200:
    localidad = response.json()
    print(localidad)
elif response.status_code == 404:
    print('Localidad no encontrada')
else:
    print(f'Error en la solicitud: {response.status_code}')