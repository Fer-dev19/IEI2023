import sqlite3
import json

conn = sqlite3.connect('../baseDatos.db')
cursor = conn.cursor()

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
        nombre TEXT PRIMARY KEY,
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

def insert_provincia(codigo, nombre):
    cursor.execute('INSERT OR IGNORE INTO Provincia (codigo, nombre) VALUES (?, ?)', (codigo, nombre))

def insert_localidad(codigo, nombre, provincia):
    cursor.execute('INSERT OR IGNORE INTO Localidad (codigo, nombre, provincia) VALUES (?, ?, ?)', (codigo, nombre, provincia))

def insert_centro_educativo(nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad):
    cursor.execute('''
        INSERT OR IGNORE INTO Centro_Educativo (nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad))

with open('../archivosJSON/CAT.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

    for entry in data:
        codigo_provincia = int(entry['codi_postal'][:2])
        nombre_provincia = {
            '8': 'Barcelona',
            '17': 'Girona',
            '25': 'Lleida',
            '43': 'Tarragona'
        }.get(str(codigo_provincia), 'Desconocida')

        codigo_localidad = int(entry['codi_municipi_6_digits']) if len(entry['codi_municipi_6_digits']) == 6 else int('0' + entry['codi_municipi_6_digits'][:5])

        insert_provincia(codigo_provincia, nombre_provincia)
        insert_localidad(codigo_localidad, entry['nom_municipi'], codigo_provincia)

        if entry['nom_naturalesa'] == 'Públic':
            tipo_centro = 'Público'
        elif entry['nom_naturalesa'] == 'Privat':
            tipo_centro = 'Privado'
        else: tipo_centro = None
        descripcion_centro = f"{entry['estudis']}, {entry['nom_titularitat']}"

        insert_centro_educativo(
            entry['denominaci_completa'],
            tipo_centro,
            entry['adre_a'],
            entry['codi_postal'],
            float(entry['coordenades_geo_x']),
            float(entry['coordenades_geo_y']),
            None,
            descripcion_centro,
            codigo_localidad
        )

conn.commit()
conn.close()
