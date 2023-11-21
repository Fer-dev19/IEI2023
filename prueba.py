import json
# Cargar datos desde el archivo JSON
with open('./xmltojson.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

    for entry in data:
        # Verificar si 'codi_postal' existe en el diccionario
        if 'codigopostal' in entry:
            # Transformaciones según las especificaciones
            codigo_provincia = int(entry['codigopostal'][:2])
            # Resto del código...
        else:
            print(f"La entrada {entry} no tiene la clave 'codigopostal'")
