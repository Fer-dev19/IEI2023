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
        FOREIGN KEY (provincia) REFERENCES Provincia (codigo)
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
        FOREIGN KEY (localidad) REFERENCES Localidad (codigo)
    )
''')

with open('../archivosJSON/MUR.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

def obtener_tipo(titularidad):
    if titularidad == 'P':
        return 'público'
    elif titularidad == 'N':
        return 'privado'
    elif titularidad == 'C':
        return 'concertado'
    else:
        return None

for centro in data:
    codigo_localidad = int(centro['cpcen']) if centro.get('cpcen') and centro['cpcen'].isdigit() else None

    cursor.execute('INSERT OR IGNORE INTO Provincia VALUES (?, ?)', (30, 'Murcia'))

    cursor.execute('INSERT OR IGNORE INTO Localidad VALUES (?, ?, ?)', (codigo_localidad, centro['loccen'], 30))

    cursor.execute('''
    INSERT OR IGNORE INTO Centro_Educativo (nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
    centro['denLarga'] + ' ' + centro['dencen'],
    obtener_tipo(centro['titularidad']),
    centro['domcen'],
    centro['cpcen'],
    centro['geo-referencia']['lon'],
    centro['geo-referencia']['lat'],
    centro['telcen'],
    centro['presentacionCorta'] + ' ' + centro['web'],
    centro['cpcen']
))

conn.commit()
conn.close()
