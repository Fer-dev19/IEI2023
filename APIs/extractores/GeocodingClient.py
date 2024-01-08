import googlemaps

class GeocodingClient:
    def __init__(self, api_key):
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