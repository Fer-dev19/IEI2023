import sqlite3
import json

# Conexión a la base de datos SQLite
conn = sqlite3.connect('baseDatos.db')
cursor = conn.cursor()

# Crear tablas si no existen
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Provincia (
        codigo TEXT PRIMARY KEY,
        nombre TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Localidad (
        codigo TEXT PRIMARY KEY,
        nombre TEXT,
        provincia TEXT,
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
        localidad TEXT,
        FOREIGN KEY (localidad) REFERENCES Localidad (codigo)
    )
''')

# Cargar datos desde el archivo JSON
with open('datos_csv_CV.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Función para obtener el tipo correcto
def obtener_tipo(regimen):
    if regimen == 'PÚB.':
        return 'público'
    elif regimen == 'PRIV. CONC.':
        return 'concertado'
    elif regimen == 'PRIV.':
        return 'privado'
    elif regimen == 'OTROS':
        return 'otros'
    else:
        return None

# Insertar datos en las tablas
for centro in data:
    # Insertar en la tabla Provincia
    cursor.execute('INSERT OR IGNORE INTO Provincia VALUES (?, ?)', (centro['CODIGO_POSTAL'], centro['PROVINCIA']))

    # Insertar en la tabla Localidad
    cursor.execute('INSERT OR IGNORE INTO Localidad VALUES (?, ?, ?)', (0, centro['LOCALIDAD'], centro['CODIGO_POSTAL']))

    # Insertar en la tabla Centro_Educativo
    cursor.execute('''
        INSERT INTO Centro_Educativo VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        centro['DENOMINACION'],
        obtener_tipo(centro['REGIMEN']),
        f"{centro['TIPO_VIA']} {centro['DIRECCION']} {centro['NUMERO']}",
        centro['CODIGO_POSTAL'],
        0,  # Longitud
        0,  # Latitud
        centro['TELEFONO'],
        f"{centro['DENOMINACION_GENERICA_ES']} {centro['DENOMINACION_GENERICA_VAL']} {centro['DENOMINACION_ESPECIFICA']} {centro['URL_ES']}",
        centro['CODIGO']
    ))

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()
