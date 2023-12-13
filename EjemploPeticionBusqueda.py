# Ejemplo de petición
import requests

url = 'http://127.0.0.1:5000/buscarLocalidad'
params = {'localidad': 'ala'}
response = requests.get(url, params=params)

if response.status_code == 200:
    # La solicitud fue exitosa
    localidad = response.json()
    print(localidad)
elif response.status_code == 404:
    print('Localidad no encontrada')
else:
    print(f'Error en la solicitud: {response.status_code}')