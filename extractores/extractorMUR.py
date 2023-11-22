import sqlite3
import json

# Conexión a la base de datos SQLite
conn = sqlite3.connect('../baseDatos.db')
cursor = conn.cursor()

# Crear tablas si no existen
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
        nombre TEXT,
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

# Cargar datos desde el archivo JSON
with open('../datos_json_MUR.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Función para obtener el tipo correcto
def obtener_tipo(titularidad):
    if titularidad == 'P':
        return 'público'
    elif titularidad == 'N':
        return 'privado'
    elif titularidad == 'C':
        return 'concertado'
    else:
        return None

# Insertar datos en las tablas
for centro in data:
    # Obtener el primer dígito del código postal según las tres posibilidades
    if len(centro['cpcen']) == 5:
        codigo_provincia = centro['cpcen'][:2]
    elif len(centro['cpcen']) == 4:
        codigo_provincia = centro['cpcen'][:1]

    # Insertar en la tabla Provincia
    cursor.execute('INSERT OR IGNORE INTO Provincia VALUES (?, ?)', (codigo_provincia, 'Murcia'))

    # Insertar en la tabla Localidad
    cursor.execute('INSERT OR IGNORE INTO Localidad VALUES (?, ?, ?)', (centro['cpcen'], centro['loccen'], codigo_provincia))

    # Insertar en la tabla Centro_Educativo
cursor.execute('''
    INSERT INTO Centro_Educativo VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    centro['denLarga'] + ' ' + centro['dencen'],
    obtener_tipo(centro['titularidad']),
    centro['domcen'],
    centro['cpcen'],
    centro['geo-referencia']['lon'],  # Corregir aquí
    centro['geo-referencia']['lat'],  # Corregir aquí
    centro['telcen'],
    centro['presentacionCorta'] + ' ' + centro['web'],
    centro['cpcen']
))

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()
