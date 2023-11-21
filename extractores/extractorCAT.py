import sqlite3
import json

# Conexión a la base de datos SQLite
conn = sqlite3.connect('../baseDatos.db')
cursor = conn.cursor()

# Crear las tablas si no existen
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Provincia (
        codigo INTEGER PRIMARY KEY,
        nombre TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Localidad (
        codigo INTEGER PRIMARY KEY,
        nombre TEXT,
        provincia INTEGER,
        FOREIGN KEY (provincia) REFERENCES Provincia(codigo)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Centro_Educativo (
        nombre TEXT,
        tipo TEXT,
        direccion TEXT,
        codigo_postal TEXT,
        longitud REAL,
        latitud REAL,
        telefono TEXT,
        descripcion TEXT,
        localidad INTEGER,
        FOREIGN KEY (localidad) REFERENCES Localidad(codigo)
    )
''')

# Función para insertar provincia en la base de datos
def insert_provincia(codigo, nombre):
    cursor.execute('INSERT INTO Provincia (codigo, nombre) VALUES (?, ?)', (codigo, nombre))

# Función para insertar localidad en la base de datos
def insert_localidad(codigo, nombre, provincia):
    cursor.execute('INSERT INTO Localidad (codigo, nombre, provincia) VALUES (?, ?, ?)', (codigo, nombre, provincia))

# Función para insertar centro educativo en la base de datos
def insert_centro_educativo(nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad):
    cursor.execute('''
        INSERT INTO Centro_Educativo (nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad))

# Cargar datos desde el archivo JSON
with open('../datos_xml_CAT.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

    for entry in data:
        # Transformaciones según las especificaciones
        codigo_provincia = int(entry['codi_postal'][:2])
        nombre_provincia = {
            '08': 'Barcelona',
            '17': 'Girona',
            '25': 'Lleida',
            '32': 'Tarragona'
        }.get(str(codigo_provincia), 'Desconocida')

        codigo_localidad = int(entry['codi_municipi_6_digits']) if len(entry['codi_municipi_6_digits']) == 6 else int('0' + entry['codi_municipi_6_digits'][:5])

        # Insertar datos en las tablas
        insert_provincia(codigo_provincia, nombre_provincia)
        insert_localidad(codigo_localidad, entry['nom_municipi'], codigo_provincia)

        tipo_centro = 'Público' if entry['nom_naturalesa'] == 'Públic' else 'Privado'
        descripcion_centro = f"{entry['estudis']}, {entry['nom_titularitat']}"

        insert_centro_educativo(
            entry['denominaci_completa'],
            tipo_centro,
            entry['adre_a'],
            entry['codi_postal'],
            float(entry['coordenades_geo_x']),
            float(entry['coordenades_geo_y']),
            '0',
            descripcion_centro,
            codigo_localidad
        )

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()