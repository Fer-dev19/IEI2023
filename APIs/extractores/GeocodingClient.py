import os
import googlemaps

#Esta clase nos permite obtener las coordenadas de Valencia debido a que
#la web de coordenadas que utilizábamos no está funcionando bien.
class GeocodingClient:
    #Es el método "constructor" de la clase
    #La API está añadida a las variables de entorno para no vulnerarla al subirla a un repositorio
    def __init__(self):
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("La clave de API de Google no está definida en las variables de entorno.")
        self.client = googlemaps.Client(key=api_key)

    def get_coordinates(self, address):
        try:
            # Realiza la solicitud de geocodificación
            result = self.client.geocode(address)

            # Verifica si se obtuvieron resultados
            if not result:
                return None

            # Extrae las coordenadas
            location = result[0]["geometry"]["location"]
            return location["lat"], location["lng"]
        except Exception as e:
            print("Error al obtener coordenadas:", e)
            return None