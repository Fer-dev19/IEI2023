import sqlite3
import json

class ExtractorMUR:
    def __init__(self, db_path, json_path):
        self.db_path = db_path
        self.json_path = json_path
        self.conn = None

    def conectar_a_base_datos(self):
        self.conn = sqlite3.connect(self.db_path)

    def cerrar_conexion_base_datos(self):
        if self.conn:
            self.conn.close()

    def crear_tablas(self):
        cursor = self.conn.cursor()
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
        self.conn.commit()

    def insertar_datos(self, data):
        # Suponemos que la lógica de obtención del tipo de centro ya está definida en una función obtener_tipo()
        for centro in data:
            codigo_postal = centro['cpcen'] if centro['cpcen'] else None
            codigo_localidad = int(codigo_postal) if codigo_postal and codigo_postal.isdigit() else None
            cursor = self.conn.cursor()
            cursor.execute('INSERT OR IGNORE INTO Provincia VALUES (?, ?)', (30, 'Murcia'))
            cursor.execute('INSERT OR IGNORE INTO Localidad VALUES (?, ?, ?)', (codigo_localidad, centro['loccen'], 30))
            cursor.execute('''
                INSERT OR IGNORE INTO Centro_Educativo (nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                centro['denLarga'] + ' ' + centro['dencen'],
                self.obtener_tipo(centro['titularidad']),
                centro['domcen'],
                codigo_postal,
                centro['geo-referencia']['lon'],
                centro['geo-referencia']['lat'],
                centro['telcen'],
                centro['presentacionCorta'] + ' ' + centro['web'],
                codigo_localidad
            ))
            self.conn.commit()

    def leer_archivo_json(self):
        with open(self.json_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def obtener_tipo(self, titularidad):
        return {
            'P': 'Público',
            'N': 'Privado',
            'C': 'Concertado'
        }.get(titularidad, None)

    def ejecutar(self):
        try:
            self.conectar_a_base_datos()
            self.crear_tablas()
            data = self.leer_archivo_json()
            self.insertar_datos(data)
        finally:
            self.cerrar_conexion_base_datos()

# Ejemplo de uso de la clase ExtractorMUR:
# extractor_mur = ExtractorMUR('../baseDatos.db', '../archivosJSON/MUR.json')
# extractor_mur.ejecutar()


# import sqlite3
# import json

# conn = sqlite3.connect('../baseDatos.db')
# cursor = conn.cursor()

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Provincia (
#         codigo INTEGER PRIMARY KEY,
#         nombre TEXT
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Localidad (
#         codigo INTEGER PRIMARY KEY,
#         nombre TEXT,
#         provincia INTEGER,
#         FOREIGN KEY (provincia) REFERENCES Provincia (codigo)
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Centro_Educativo (
#         nombre TEXT PRIMARY KEY,
#         tipo TEXT,
#         direccion TEXT,
#         codigo_postal TEXT,
#         longitud REAL,
#         latitud REAL,
#         telefono TEXT,
#         descripcion TEXT,
#         localidad INTEGER,
#         FOREIGN KEY (localidad) REFERENCES Localidad (codigo)
#     )
# ''')

# with open('../archivosJSON/MUR.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)

# def obtener_tipo(titularidad):
#     if titularidad == 'P':
#         return 'Público'
#     elif titularidad == 'N':
#         return 'Privado'
#     elif titularidad == 'C':
#         return 'Concertado'
#     else:
#         return None

# for centro in data:
#     if centro['cpcen'] == "":
#         codigo_postal = None
#     else: codigo_postal = centro['cpcen']

#     codigo_localidad = int(centro['cpcen']) if centro.get('cpcen') and centro['cpcen'].isdigit() else None

#     cursor.execute('INSERT OR IGNORE INTO Provincia VALUES (?, ?)', (30, 'Murcia'))

#     cursor.execute('INSERT OR IGNORE INTO Localidad VALUES (?, ?, ?)', (codigo_localidad, centro['loccen'], 30))

#     cursor.execute('''
#     INSERT OR IGNORE INTO Centro_Educativo (nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad) 
#                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#     ''', (
#     centro['denLarga'] + ' ' + centro['dencen'],
#     obtener_tipo(centro['titularidad']),
#     centro['domcen'],
#     codigo_postal,
#     centro['geo-referencia']['lon'],
#     centro['geo-referencia']['lat'],
#     centro['telcen'],
#     centro['presentacionCorta'] + ' ' + centro['web'],
#     codigo_localidad
# ))

# conn.commit()
# conn.close()
